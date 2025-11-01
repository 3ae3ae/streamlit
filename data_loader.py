"""
Data loader module for MongoDB JSON exports.
Handles loading and parsing of JSON files from the data directory.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Data directory path
DATA_DIR = Path("data")


def parse_mongodb_date(date_obj: Any) -> Optional[datetime]:
    """
    Convert MongoDB $date format to datetime object.
    
    Args:
        date_obj: MongoDB date object with $date field or datetime string
        
    Returns:
        datetime object or None if parsing fails
    """
    if date_obj is None:
        return None
    
    try:
        if isinstance(date_obj, dict) and "$date" in date_obj:
            date_str = date_obj["$date"]
            # Handle ISO 8601 format
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        elif isinstance(date_obj, str):
            return datetime.fromisoformat(date_obj.replace("Z", "+00:00"))
        else:
            return None
    except (ValueError, AttributeError) as e:
        logger.warning(f"Failed to parse date: {date_obj}, error: {e}")
        return None


def parse_mongodb_oid(oid_obj: Any) -> Optional[str]:
    """
    Convert MongoDB $oid format to string.
    
    Args:
        oid_obj: MongoDB ObjectId with $oid field or string
        
    Returns:
        ObjectId as string or None if parsing fails
    """
    if oid_obj is None:
        return None
    
    try:
        if isinstance(oid_obj, dict) and "$oid" in oid_obj:
            return oid_obj["$oid"]
        elif isinstance(oid_obj, str):
            return oid_obj
        else:
            return None
    except (KeyError, AttributeError) as e:
        logger.warning(f"Failed to parse ObjectId: {oid_obj}, error: {e}")
        return None


def load_json_file(filename: str) -> List[Dict[str, Any]]:
    """
    Load JSON file from data directory with error handling.
    
    Args:
        filename: Name of the JSON file to load
        
    Returns:
        List of dictionaries from JSON file
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file contains invalid JSON
    """
    file_path = DATA_DIR / filename
    
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"데이터 파일을 찾을 수 없습니다: {filename}")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info(f"Successfully loaded {filename}: {len(data)} records")
            return data
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON file {filename}: {e}")
        raise json.JSONDecodeError(
            f"JSON 파싱 오류: {filename}",
            e.doc,
            e.pos
        )
    except Exception as e:
        logger.error(f"Unexpected error loading {filename}: {e}")
        raise



@st.cache_data
def load_users() -> pd.DataFrame:
    """
    Load users data from prod.users.json.
    
    Returns:
        DataFrame with user information including political preferences
    """
    try:
        data = load_json_file("prod.users.json")
        
        if not data:
            logger.warning("No user data found in file")
            return pd.DataFrame()
        
        # Parse MongoDB fields
        for record in data:
            if "_id" in record:
                record["_id"] = parse_mongodb_oid(record["_id"])
            if "createdAt" in record:
                record["createdAt"] = parse_mongodb_date(record["createdAt"])
            if "updatedAt" in record:
                record["updatedAt"] = parse_mongodb_date(record["updatedAt"])
        
        df = pd.DataFrame(data)
        logger.info(f"Loaded {len(df)} users")
        return df
    except FileNotFoundError as e:
        logger.error(f"User data file not found: {e}")
        return pd.DataFrame()
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in user data file: {e}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error loading users: {e}", exc_info=True)
        return pd.DataFrame()


@st.cache_data
def load_political_score_history() -> pd.DataFrame:
    """
    Load political score history from prod.userPoliticalScoreHistory.json.
    
    Returns:
        DataFrame with user political score history across categories
    """
    try:
        data = load_json_file("prod.userPoliticalScoreHistory.json")
        
        if not data:
            logger.warning("No political score history data found in file")
            return pd.DataFrame()
        
        # Parse MongoDB fields and flatten nested score objects
        records = []
        for record in data:
            try:
                flat_record = {
                    "_id": parse_mongodb_oid(record.get("_id")),
                    "userId": record.get("userId"),
                    "createdAt": parse_mongodb_date(record.get("createdAt"))
                }
                
                # Flatten category scores
                for category in ["politics", "economy", "society", "culture", "technology", "international"]:
                    if category in record and isinstance(record[category], dict):
                        flat_record[f"{category}_left"] = record[category].get("left", 50)
                        flat_record[f"{category}_center"] = record[category].get("center", 50)
                        flat_record[f"{category}_right"] = record[category].get("right", 50)
                
                records.append(flat_record)
            except Exception as e:
                logger.warning(f"Skipping invalid record: {e}")
                continue
        
        if not records:
            logger.warning("No valid political score history records found")
            return pd.DataFrame()
        
        df = pd.DataFrame(records)
        logger.info(f"Loaded {len(df)} political score history records")
        return df
    except FileNotFoundError as e:
        logger.error(f"Political score history file not found: {e}")
        return pd.DataFrame()
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in political score history file: {e}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error loading political score history: {e}", exc_info=True)
        return pd.DataFrame()


@st.cache_data
def load_topics() -> pd.DataFrame:
    """
    Load topics from prod.topics.json.
    
    Returns:
        DataFrame with topic information
    """
    try:
        data = load_json_file("prod.topics.json")
        
        # Parse MongoDB fields
        for record in data:
            if "createdAt" in record:
                record["createdAt"] = parse_mongodb_date(record["createdAt"])
            if "updatedAt" in record:
                record["updatedAt"] = parse_mongodb_date(record["updatedAt"])
            if "deletedAt" in record:
                record["deletedAt"] = parse_mongodb_date(record["deletedAt"])
        
        df = pd.DataFrame(data)
        logger.info(f"Loaded {len(df)} topics")
        return df
    except Exception as e:
        logger.error(f"Error loading topics: {e}")
        st.error(f"토픽 데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame()


@st.cache_data
def load_topic_subscriptions() -> pd.DataFrame:
    """
    Load topic subscriptions from prod.userTopicSubscriptions.json.
    
    Returns:
        DataFrame with user topic subscription information
    """
    try:
        data = load_json_file("prod.userTopicSubscriptions.json")
        
        # Parse MongoDB fields
        for record in data:
            if "_id" in record:
                record["_id"] = parse_mongodb_oid(record["_id"])
            if "subscribedAt" in record:
                record["subscribedAt"] = parse_mongodb_date(record["subscribedAt"])
        
        df = pd.DataFrame(data)
        logger.info(f"Loaded {len(df)} topic subscriptions")
        return df
    except Exception as e:
        logger.error(f"Error loading topic subscriptions: {e}")
        st.error(f"토픽 구독 데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame()


@st.cache_data
def load_issues() -> pd.DataFrame:
    """
    Load issues from prod.issues.json.
    
    Returns:
        DataFrame with issue information
    """
    try:
        data = load_json_file("prod.issues.json")
        
        # Parse MongoDB fields
        for record in data:
            if "createdAt" in record:
                record["createdAt"] = parse_mongodb_date(record["createdAt"])
            if "updatedAt" in record:
                record["updatedAt"] = parse_mongodb_date(record["updatedAt"])
        
        df = pd.DataFrame(data)
        logger.info(f"Loaded {len(df)} issues")
        return df
    except Exception as e:
        logger.error(f"Error loading issues: {e}")
        st.error(f"이슈 데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame()


@st.cache_data
def load_issue_comments() -> pd.DataFrame:
    """
    Load issue comments from prod.issueComments.json.
    
    Returns:
        DataFrame with issue comment information
    """
    try:
        data = load_json_file("prod.issueComments.json")
        
        for record in data:
            if "_id" in record:
                record["_id"] = parse_mongodb_oid(record["_id"])
            if "createdAt" in record:
                record["createdAt"] = parse_mongodb_date(record["createdAt"])
            if "updatedAt" in record:
                record["updatedAt"] = parse_mongodb_date(record.get("updatedAt"))
        
        df = pd.DataFrame(data)
        logger.info(f"Loaded {len(df)} issue comments")
        return df
    except Exception as e:
        logger.error(f"Error loading issue comments: {e}")
        st.error(f"댓글 데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame()


@st.cache_data
def load_issue_evaluations() -> pd.DataFrame:
    """
    Load issue evaluations from prod.userIssueEvaluations.json.
    
    Returns:
        DataFrame with user issue evaluation information
    """
    try:
        data = load_json_file("prod.userIssueEvaluations.json")
        
        # Parse MongoDB fields
        for record in data:
            if "_id" in record:
                record["_id"] = parse_mongodb_oid(record["_id"])
            if "evaluatedAt" in record:
                record["evaluatedAt"] = parse_mongodb_date(record["evaluatedAt"])
        
        df = pd.DataFrame(data)
        logger.info(f"Loaded {len(df)} issue evaluations")
        return df
    except Exception as e:
        logger.error(f"Error loading issue evaluations: {e}")
        st.error(f"이슈 평가 데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame()


@st.cache_data
def load_user_watch_history() -> pd.DataFrame:
    """
    Load user watch history from prod.userWatchHistory.json.
    
    Returns:
        DataFrame with user watch history information
    """
    try:
        data = load_json_file("prod.userWatchHistory.json")
        
        # Parse MongoDB fields
        for record in data:
            if "_id" in record:
                record["_id"] = parse_mongodb_oid(record["_id"])
            if "watchedAt" in record:
                record["watchedAt"] = parse_mongodb_date(record["watchedAt"])
        
        df = pd.DataFrame(data)
        logger.info(f"Loaded {len(df)} watch history records")
        return df
    except Exception as e:
        logger.error(f"Error loading user watch history: {e}")
        st.error(f"시청 기록 데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame()


@st.cache_data
def load_user_comment_likes() -> pd.DataFrame:
    """
    Load user comment likes from prod.userCommentLikes.json.
    
    Returns:
        DataFrame with user comment like information
    """
    try:
        data = load_json_file("prod.userCommentLikes.json")
        
        for record in data:
            if "_id" in record:
                record["_id"] = parse_mongodb_oid(record["_id"])
            if "likedAt" in record:
                record["likedAt"] = parse_mongodb_date(record["likedAt"])
        
        df = pd.DataFrame(data)
        logger.info(f"Loaded {len(df)} user comment likes")
        return df
    except Exception as e:
        logger.error(f"Error loading user comment likes: {e}")
        st.error(f"댓글 좋아요 데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame()


@st.cache_data
def load_media_sources() -> pd.DataFrame:
    """
    Load media sources from prod.mediaSources.json.
    
    Returns:
        DataFrame with media source information
    """
    try:
        data = load_json_file("prod.mediaSources.json")
        
        # Parse MongoDB fields if present
        for record in data:
            if "createdAt" in record:
                record["createdAt"] = parse_mongodb_date(record["createdAt"])
            if "updatedAt" in record:
                record["updatedAt"] = parse_mongodb_date(record["updatedAt"])
        
        df = pd.DataFrame(data)
        logger.info(f"Loaded {len(df)} media sources")
        return df
    except Exception as e:
        logger.error(f"Error loading media sources: {e}")
        st.error(f"언론사 데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame()
