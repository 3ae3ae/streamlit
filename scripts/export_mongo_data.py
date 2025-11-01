#!/usr/bin/env python3
"""
CLI helper to export project datasets from MongoDB using PyMongo.

The export rules mirror the visualization project requirements:
* users: only entries where updatedAt - createdAt >= 1 hour, with a limited field set.
* user* collections: only documents tied to the filtered users.
* issues: only available issues published within the recent lookback window,
  excluding clusterMetadata.
* issue comments: only comments for the exported issues.
* topics: full export.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable, Sequence

from bson import json_util
from pymongo import MongoClient

DEFAULT_COLLECTION_PREFIX = "user"
DEFAULT_CHUNK_SIZE = 200
DEFAULT_USER_ID_FIELD = "userId"
DEFAULT_ISSUE_COMMENTS_COLLECTION = "issueComments"
DEFAULT_ISSUE_ID_FIELD = "issueId"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export MongoDB documents required by the visualization project."
    )
    parser.add_argument("--uri", required=True, help="MongoDB connection string.")
    parser.add_argument("--db", required=True, help="Database name to export from.")
    parser.add_argument(
        "--data-dir",
        default="data",
        help="Output directory for exported JSON files (default: data).",
    )
    parser.add_argument(
        "--issue-lookback-days",
        type=int,
        default=90,
        help="Only export issues published within this many recent days (default: 90).",
    )
    parser.add_argument(
        "--user-collection-prefix",
        default=DEFAULT_COLLECTION_PREFIX,
        help="Export additional collections whose names start with this prefix (default: user).",
    )
    parser.add_argument(
        "--user-id-field",
        default=DEFAULT_USER_ID_FIELD,
        help="Field name that stores the user identifier in user* collections (default: userId).",
    )
    parser.add_argument(
        "--chunk-size",
        "--user-chunk-size",
        dest="chunk_size",
        type=int,
        default=DEFAULT_CHUNK_SIZE,
        help="Maximum number of identifiers per $in query when exporting related documents (default: 200).",
    )
    parser.add_argument(
        "--issue-comments-collection",
        default=DEFAULT_ISSUE_COMMENTS_COLLECTION,
        help="Collection name for issue comments (default: issueComments).",
    )
    parser.add_argument(
        "--issue-comment-id-field",
        default=DEFAULT_ISSUE_ID_FIELD,
        help="Field name that links issue comments to issues (default: issueId).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging.",
    )
    return parser.parse_args()


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def build_users_filter() -> dict:
    return {
        "$expr": {
            "$gte": [
                {"$abs": {"$subtract": ["$updatedAt", "$createdAt"]}},
                60 * 60 * 1000,
            ]
        }
    }


def build_issues_filter(lookback_days: int) -> dict:
    threshold = datetime.utcnow() - timedelta(days=lookback_days)
    return {
        "isAvailable": True,
        "publishedAt": {"$gte": threshold},
    }


def chunked(seq: Sequence[str], size: int) -> Iterable[Sequence[str]]:
    step = max(size, 1)
    for start in range(0, len(seq), step):
        yield seq[start : start + step]


def write_json_array(path: Path, payload) -> None:
    with path.open("w", encoding="utf-8") as handle:
        handle.write(json_util.dumps(list(payload), ensure_ascii=True, indent=2))
        handle.write("\n")


def resolve_user_collections(client: MongoClient, db_name: str, prefix: str) -> list[str]:
    collections = client[db_name].list_collection_names()
    lower_prefix = prefix.lower()
    return sorted(
        name
        for name in collections
        if name.lower().startswith(lower_prefix) and name != "users"
    )


def export_users(
    client: MongoClient,
    db_name: str,
    data_dir: Path,
    user_filter: dict,
    verbose: bool,
) -> list[str]:
    target = data_dir / f"{db_name}.users.json"
    if verbose:
        print(f"Exporting users to {target}")
    projection = {
        "_id": 0,
        "politicalPreference": 1,
        "id": 1,
        "createdAt": 1,
        "updatedAt": 1,
    }
    cursor = client[db_name]["users"].find(user_filter, projection).sort("id", 1)
    docs = list(cursor)
    write_json_array(target, docs)
    user_ids = sorted({doc["id"] for doc in docs if "id" in doc})
    if verbose:
        print(f"Identified {len(user_ids)} filtered users")
    return user_ids


def export_user_related_collection(
    client: MongoClient,
    db_name: str,
    data_dir: Path,
    collection: str,
    user_ids: Sequence[str],
    user_id_field: str,
    chunk_size: int,
    verbose: bool,
) -> None:
    target = data_dir / f"{db_name}.{collection}.json"
    if not user_ids:
        if verbose:
            print(f"No matching users; writing empty dataset for {collection}")
        write_json_array(target, [])
        return

    documents = []
    for idx, chunk in enumerate(chunked(user_ids, chunk_size), start=1):
        if verbose:
            print(f"  chunk {idx}: exporting {len(chunk)} user IDs from {collection}")
        query = {user_id_field: {"$in": list(chunk)}}
        documents.extend(client[db_name][collection].find(query))

    write_json_array(target, documents)
    if verbose:
        print(f"Wrote {len(documents)} documents to {target}")


def export_issues(
    client: MongoClient,
    db_name: str,
    data_dir: Path,
    lookback_days: int,
    verbose: bool,
) -> list[str]:
    target = data_dir / f"{db_name}.issues.json"
    if verbose:
        print(f"Exporting filtered issues to {target}")
    issues_filter = build_issues_filter(lookback_days)
    documents = []
    for doc in client[db_name]["issues"].find(issues_filter):
        material = dict(doc)
        material.pop("clusterMetadata", None)
        documents.append(material)

    write_json_array(target, documents)
    issue_ids = sorted({str(doc["_id"]) for doc in documents if "_id" in doc})
    if verbose:
        print(f"Collected {len(issue_ids)} issue identifiers")
    return issue_ids


def export_issue_comments(
    client: MongoClient,
    db_name: str,
    data_dir: Path,
    collection: str,
    issue_ids: Sequence[str],
    issue_id_field: str,
    chunk_size: int,
    verbose: bool,
) -> None:
    target = data_dir / f"{db_name}.{collection}.json"
    if not issue_ids:
        if verbose:
            print(f"No issues exported; writing empty dataset for {collection}")
        write_json_array(target, [])
        return

    documents = []
    for idx, chunk in enumerate(chunked(issue_ids, chunk_size), start=1):
        if verbose:
            print(f"  chunk {idx}: exporting {len(chunk)} issue IDs from {collection}")
        query = {issue_id_field: {"$in": list(chunk)}}
        documents.extend(client[db_name][collection].find(query))

    write_json_array(target, documents)
    if verbose:
        print(f"Wrote {len(documents)} documents to {target}")


def export_topics(
    client: MongoClient,
    db_name: str,
    data_dir: Path,
    verbose: bool,
) -> None:
    target = data_dir / f"{db_name}.topics.json"
    if verbose:
        print(f"Exporting all topics to {target}")
    documents = list(client[db_name]["topics"].find())
    write_json_array(target, documents)


def main() -> int:
    args = parse_args()
    data_dir = Path(args.data_dir)
    ensure_directory(data_dir)

    try:
        client = MongoClient(args.uri)
    except Exception as exc:
        raise SystemExit(f"Failed to connect to MongoDB: {exc}") from exc

    user_filter = build_users_filter()
    user_ids = export_users(
        client=client,
        db_name=args.db,
        data_dir=data_dir,
        user_filter=user_filter,
        verbose=args.verbose,
    )

    user_collections = resolve_user_collections(client, args.db, args.user_collection_prefix)
    if args.verbose:
        print(f"User-related collections: {', '.join(user_collections) or '(none)'}")

    for collection in user_collections:
        export_user_related_collection(
            client=client,
            db_name=args.db,
            data_dir=data_dir,
            collection=collection,
            user_ids=user_ids,
            user_id_field=args.user_id_field,
            chunk_size=args.chunk_size,
            verbose=args.verbose,
        )

    issue_ids = export_issues(
        client=client,
        db_name=args.db,
        data_dir=data_dir,
        lookback_days=args.issue_lookback_days,
        verbose=args.verbose,
    )

    export_issue_comments(
        client=client,
        db_name=args.db,
        data_dir=data_dir,
        collection=args.issue_comments_collection,
        issue_ids=issue_ids,
        issue_id_field=args.issue_comment_id_field,
        chunk_size=args.chunk_size,
        verbose=args.verbose,
    )

    export_topics(
        client=client,
        db_name=args.db,
        data_dir=data_dir,
        verbose=args.verbose,
    )

    if args.verbose:
        print("Export completed")
    client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
