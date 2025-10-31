"""
Helper functions to build the user monthly activity report.

These utilities provide filtered datasets and aggregated metrics used by
the Streamlit page that summarizes one user's recent behavior.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)


def _ensure_datetime(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Ensure the specified column is converted to datetime if present.
    
    Args:
        df: Source DataFrame
        column: Column name to cast
    
    Returns:
        DataFrame with datetime column (copy if conversion is required)
    """
    if df.empty or column not in df.columns:
        return df
    
    if not pd.api.types.is_datetime64_any_dtype(df[column]):
        df = df.copy()
        df[column] = pd.to_datetime(df[column], errors="coerce")
    return df


def _get_time_window(
    days: int,
    reference_date: Optional[datetime] = None
) -> tuple[datetime, datetime]:
    """
    Calculate the start and end date for the recent window.
    
    Args:
        days: Number of days to look back
        reference_date: Optional anchor point (defaults to now, UTC)
    
    Returns:
        Tuple of (start_date, end_date)
    """
    end_date = reference_date or datetime.now(timezone.utc)
    if end_date.tzinfo is None:
        end_date = end_date.replace(tzinfo=timezone.utc)
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def get_user_recent_watch_history(
    watch_df: pd.DataFrame,
    user_id: str,
    days: int = 30,
    reference_date: Optional[datetime] = None
) -> pd.DataFrame:
    """
    Filter watch history for a specific user within the recent time window.
    
    Args:
        watch_df: DataFrame returned from load_user_watch_history
        user_id: Target user ID
        days: Look-back window in days
        reference_date: Optional anchor date (defaults to now)
    
    Returns:
        Filtered DataFrame sorted by watchedAt (descending)
    """
    if watch_df.empty:
        return pd.DataFrame()
    
    if "userId" not in watch_df.columns or "watchedAt" not in watch_df.columns:
        logger.warning("watch_df missing required columns for filtering")
        return pd.DataFrame()
    
    watch_df = _ensure_datetime(watch_df, "watchedAt")
    
    start_date, end_date = _get_time_window(days, reference_date)
    
    user_watch = watch_df[watch_df["userId"] == user_id].copy()
    if user_watch.empty:
        return pd.DataFrame()
    
    filtered = user_watch[
        (user_watch["watchedAt"] >= start_date) &
        (user_watch["watchedAt"] <= end_date)
    ].copy()
    
    if filtered.empty:
        return filtered
    
    filtered = filtered.sort_values("watchedAt", ascending=False)
    return filtered


def count_user_watch_by_issue(
    watch_df: pd.DataFrame,
    issues_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Aggregate watch counts per issue for the filtered watch dataframe.
    
    Args:
        watch_df: Filtered watch dataframe (single user)
        issues_df: Issues metadata dataframe
    
    Returns:
        DataFrame with columns:
            - issueId
            - watch_count
            - title
            - category
    """
    if watch_df.empty:
        return pd.DataFrame()
    
    issue_counts = (
        watch_df.groupby("issueId")
        .size()
        .reset_index(name="watch_count")
        .sort_values("watch_count", ascending=False)
    )
    
    if issues_df.empty or "_id" not in issues_df.columns:
        issue_counts["title"] = None
        issue_counts["category"] = None
        return issue_counts
    
    issue_meta = issues_df[["_id", "title", "category"]].copy()
    issue_meta = issue_meta.rename(columns={"_id": "issueId"})
    
    result = issue_counts.merge(issue_meta, on="issueId", how="left")
    result["category"] = result["category"].fillna("unknown")
    return result


def count_watch_by_category(issue_counts: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate watch counts by issue category.
    
    Args:
        issue_counts: DataFrame produced by count_user_watch_by_issue
    
    Returns:
        DataFrame with columns:
            - category
            - watch_count
    """
    if issue_counts.empty or "category" not in issue_counts.columns:
        return pd.DataFrame()
    
    category_counts = (
        issue_counts.groupby("category")["watch_count"]
        .sum()
        .reset_index()
        .sort_values("watch_count", ascending=False)
    )
    return category_counts


def count_watch_by_day(watch_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate watch counts by date for the filtered watch dataframe.
    
    Args:
        watch_df: Filtered watch dataframe (single user)
    
    Returns:
        DataFrame with columns:
            - date: datetime
            - watch_count: int
    """
    if watch_df.empty or "watchedAt" not in watch_df.columns:
        return pd.DataFrame()
    
    watch_df = _ensure_datetime(watch_df, "watchedAt")
    if watch_df.empty:
        return pd.DataFrame()
    
    daily = watch_df.copy()
    daily["date"] = daily["watchedAt"].dt.date
    
    aggregated = (
        daily.groupby("date")
        .size()
        .reset_index(name="watch_count")
        .sort_values("date")
    )
    
    aggregated["date"] = pd.to_datetime(aggregated["date"])
    return aggregated


def filter_user_issue_evaluations(
    evaluations_df: pd.DataFrame,
    user_id: str,
    days: int = 30,
    reference_date: Optional[datetime] = None
) -> pd.DataFrame:
    """
    Filter issue evaluations for the target user in the recent window.
    
    Args:
        evaluations_df: DataFrame from load_issue_evaluations
        user_id: Target user ID
        days: Look-back window in days
        reference_date: Optional anchor date (defaults to now)
    
    Returns:
        Filtered DataFrame sorted by evaluatedAt (descending)
    """
    if evaluations_df.empty:
        return pd.DataFrame()
    
    required_cols = {"userId", "evaluatedAt"}
    if not required_cols.issubset(evaluations_df.columns):
        logger.warning("Issue evaluations dataframe missing required columns")
        return pd.DataFrame()
    
    evaluations_df = _ensure_datetime(evaluations_df, "evaluatedAt")
    
    start_date, end_date = _get_time_window(days, reference_date)
    
    user_evals = evaluations_df[evaluations_df["userId"] == user_id].copy()
    if user_evals.empty:
        return pd.DataFrame()
    
    filtered = user_evals[
        (user_evals["evaluatedAt"] >= start_date) &
        (user_evals["evaluatedAt"] <= end_date)
    ].copy()
    
    if filtered.empty:
        return filtered
    
    filtered = filtered.sort_values("evaluatedAt", ascending=False)
    return filtered


def count_evaluations_by_perspective(
    evaluations_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Count how many evaluations fall into each perspective bucket.
    
    Args:
        evaluations_df: Filtered evaluations dataframe
    
    Returns:
        DataFrame with columns:
            - perspective
            - evaluation_count
    """
    if evaluations_df.empty or "perspective" not in evaluations_df.columns:
        return pd.DataFrame()
    
    perspective_counts = (
        evaluations_df["perspective"]
        .fillna("unknown")
        .value_counts()
        .rename_axis("perspective")
        .reset_index(name="evaluation_count")
    )
    return perspective_counts


def filter_user_political_scores(
    score_history_df: pd.DataFrame,
    user_id: str,
    days: int = 30,
    reference_date: Optional[datetime] = None
) -> pd.DataFrame:
    """
    Filter political score history for a user within the recent window.
    
    Args:
        score_history_df: DataFrame from load_political_score_history
        user_id: Target user ID
        days: Look-back window in days
        reference_date: Optional anchor date (defaults to now)
    
    Returns:
        Filtered DataFrame sorted by createdAt (ascending)
    """
    if score_history_df.empty:
        return pd.DataFrame()
    
    required_cols = {"userId", "createdAt"}
    if not required_cols.issubset(score_history_df.columns):
        logger.warning("Political score history missing required columns")
        return pd.DataFrame()
    
    score_history_df = _ensure_datetime(score_history_df, "createdAt")
    
    start_date, end_date = _get_time_window(days, reference_date)
    
    user_scores = score_history_df[score_history_df["userId"] == user_id].copy()
    if user_scores.empty:
        return pd.DataFrame()
    
    filtered = user_scores[
        (user_scores["createdAt"] >= start_date) &
        (user_scores["createdAt"] <= end_date)
    ].copy()
    
    if filtered.empty:
        return filtered
    
    filtered = filtered.sort_values("createdAt", ascending=True)
    return filtered


def summarize_media_perspectives(
    issue_counts: pd.DataFrame,
    issues_df: pd.DataFrame,
    media_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate weighted media perspective coverage for the watched issues.
    
    Args:
        issue_counts: DataFrame with per-issue watch counts (single user)
        issues_df: Issues metadata dataframe
        media_df: Media sources dataframe
    
    Returns:
        DataFrame with columns:
            - perspective
            - weighted_coverage
    """
    if issue_counts.empty:
        return pd.DataFrame()
    
    if issues_df.empty:
        logger.warning("Issues dataframe is empty; cannot summarize media perspectives")
        return pd.DataFrame()
    
    issues_lookup = issues_df.set_index("_id") if "_id" in issues_df.columns else pd.DataFrame()
    media_lookup = media_df.set_index("_id") if not media_df.empty and "_id" in media_df.columns else pd.DataFrame()
    
    records: list[dict] = []
    
    for _, row in issue_counts.iterrows():
        issue_id = row["issueId"]
        watch_count = row["watch_count"]
        
        if issues_lookup.empty or issue_id not in issues_lookup.index:
            continue
        
        issue_info = issues_lookup.loc[issue_id]
        if isinstance(issue_info, pd.DataFrame):
            issue_info = issue_info.iloc[0]
        sources = issue_info.get("sources") if hasattr(issue_info, "get") else None
        
        if sources:
            # Use source-level metadata when available
            total_sources = len(sources)
            if total_sources == 0:
                continue
            
            source_weight = watch_count / total_sources
            
            for source in sources:
                if not isinstance(source, dict):
                    continue
                
                source_id = source.get("_id")
                media_name = source.get("name")
                perspective = source.get("perspective")
                
                if not media_lookup.empty and source_id in media_lookup.index:
                    media_row = media_lookup.loc[source_id]
                    if hasattr(media_row, "get"):
                        perspective = media_row.get("perspective", perspective)
                    if media_name is None:
                        media_name = media_row.get("name")
                
                records.append({
                    "issueId": issue_id,
                    "media_id": source_id,
                    "media_name": media_name,
                    "perspective": perspective or "unknown",
                    "weight": source_weight
                })
        else:
            # Fallback to coverageSpectrum if detailed sources are missing
            coverage = issue_info.get("coverageSpectrum") if hasattr(issue_info, "get") else None
            if isinstance(coverage, dict):
                total_coverage = sum(
                    value for key, value in coverage.items()
                    if key != "total" and isinstance(value, (int, float))
                )
                if total_coverage <= 0:
                    continue
                
                for perspective_key, value in coverage.items():
                    if perspective_key == "total":
                        continue
                    if not isinstance(value, (int, float)):
                        continue
                    
                    normalized_weight = watch_count * (value / total_coverage)
                    records.append({
                        "issueId": issue_id,
                        "media_id": None,
                        "media_name": None,
                        "perspective": perspective_key or "unknown",
                        "weight": normalized_weight
                    })
    
    if not records:
        return pd.DataFrame()
    
    media_records = pd.DataFrame(records)
    media_records["perspective"] = media_records["perspective"].fillna("unknown")
    
    perspective_summary = (
        media_records.groupby("perspective")["weight"]
        .sum()
        .reset_index(name="weighted_coverage")
        .sort_values("weighted_coverage", ascending=False)
    )
    
    return perspective_summary
