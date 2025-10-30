"""
Data aggregation module for MongoDB visualization tool.
Handles aggregation and transformation of loaded data for visualization.
"""

import logging
from datetime import datetime

import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def aggregate_political_scores_by_date(
    history_df: pd.DataFrame,
    start_date: datetime,
    end_date: datetime
) -> pd.DataFrame:
    """
    Aggregate political scores by date for time-series analysis.
    
    This function processes political score history data and aggregates it by date,
    calculating the sum of left, center, and right scores for each category and date.
    It also computes the total score and proportions for visualization.
    
    Args:
        history_df: DataFrame with political score history (from load_political_score_history)
        start_date: Start date for filtering
        end_date: End date for filtering
        
    Returns:
        DataFrame with columns:
            - date: datetime
            - category: str (politics, economy, society, culture, technology, international)
            - left_score: float (sum of left scores)
            - center_score: float (sum of center scores)
            - right_score: float (sum of right scores)
            - total_score: float (sum of all scores)
            - left_proportion: float (left_score / total_score)
            - center_proportion: float (center_score / total_score)
            - right_proportion: float (right_score / total_score)
    """
    if history_df.empty:
        logger.warning("Empty history dataframe provided")
        return pd.DataFrame()
    
    if "createdAt" not in history_df.columns:
        logger.error("createdAt column not found in history dataframe")
        return pd.DataFrame()
    
    # Ensure start_date and end_date are timezone-aware if createdAt is
    if not history_df["createdAt"].empty and history_df["createdAt"].dt.tz is not None:
        # Make start_date and end_date timezone-aware (UTC)
        if start_date.tzinfo is None:
            start_date = start_date.replace(tzinfo=pd.Timestamp.now(tz='UTC').tzinfo)
        if end_date.tzinfo is None:
            end_date = end_date.replace(tzinfo=pd.Timestamp.now(tz='UTC').tzinfo)
    
    # Filter by date range
    filtered_df = history_df[
        (history_df["createdAt"] >= start_date) & 
        (history_df["createdAt"] <= end_date)
    ].copy()
    
    if filtered_df.empty:
        logger.warning(f"No data found between {start_date} and {end_date}")
        return pd.DataFrame()
    
    # Extract date only (without time)
    filtered_df["date"] = filtered_df["createdAt"].dt.date
    
    # Categories to process
    categories = ["politics", "economy", "society", "culture", "technology", "international"]
    
    # Aggregate data for each category
    aggregated_records = []
    
    for category in categories:
        left_col = f"{category}_left"
        center_col = f"{category}_center"
        right_col = f"{category}_right"
        
        # Check if columns exist
        if left_col not in filtered_df.columns:
            logger.warning(f"Column {left_col} not found, skipping category {category}")
            continue
        
        # Group by date and sum scores
        category_agg = filtered_df.groupby("date").agg({
            left_col: "sum",
            center_col: "sum",
            right_col: "sum"
        }).reset_index()
        
        # Rename columns
        category_agg.columns = ["date", "left_score", "center_score", "right_score"]
        
        # Calculate total and proportions
        category_agg["total_score"] = (
            category_agg["left_score"] + 
            category_agg["center_score"] + 
            category_agg["right_score"]
        )
        
        # Avoid division by zero
        category_agg["left_proportion"] = category_agg.apply(
            lambda row: row["left_score"] / row["total_score"] if row["total_score"] > 0 else 0,
            axis=1
        )
        category_agg["center_proportion"] = category_agg.apply(
            lambda row: row["center_score"] / row["total_score"] if row["total_score"] > 0 else 0,
            axis=1
        )
        category_agg["right_proportion"] = category_agg.apply(
            lambda row: row["right_score"] / row["total_score"] if row["total_score"] > 0 else 0,
            axis=1
        )
        
        # Add category column
        category_agg["category"] = category
        
        aggregated_records.append(category_agg)
    
    if not aggregated_records:
        logger.warning("No aggregated records created")
        return pd.DataFrame()
    
    # Combine all categories
    result_df = pd.concat(aggregated_records, ignore_index=True)
    
    # Convert date back to datetime for consistency
    result_df["date"] = pd.to_datetime(result_df["date"])
    
    # Sort by date and category
    result_df = result_df.sort_values(["date", "category"]).reset_index(drop=True)
    
    logger.info(f"Aggregated {len(result_df)} records across {len(categories)} categories")
    
    return result_df



def calculate_topic_subscriber_counts(
    topics_df: pd.DataFrame,
    subscriptions_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate subscriber count for each topic.
    
    Args:
        topics_df: DataFrame with topic information (from load_topics)
        subscriptions_df: DataFrame with user topic subscriptions (from load_topic_subscriptions)
        
    Returns:
        DataFrame with columns:
            - topic_id: str
            - topic_name: str
            - subscriber_count: int
            - category: str (if available in topics_df)
    """
    if topics_df.empty:
        logger.warning("Empty topics dataframe provided")
        return pd.DataFrame()
    
    if subscriptions_df.empty:
        logger.warning("Empty subscriptions dataframe provided")
        # Return topics with zero subscribers
        result = topics_df[["_id", "name"]].copy()
        result.columns = ["topic_id", "topic_name"]
        result["subscriber_count"] = 0
        if "category" in topics_df.columns:
            result["category"] = topics_df["category"]
        return result
    
    # Count subscriptions per topic
    subscription_counts = subscriptions_df.groupby("topicId").size().to_frame(name="subscriber_count").reset_index()
    
    # Merge with topics to get topic names
    result = topics_df[["_id", "name"]].merge(
        subscription_counts,
        left_on="_id",
        right_on="topicId",
        how="left"
    )
    
    # Fill NaN subscriber counts with 0
    result["subscriber_count"] = result["subscriber_count"].fillna(0).astype(int)
    
    # Rename columns
    result = result.rename(columns={"_id": "topic_id", "name": "topic_name"})
    
    # Add category if available
    if "category" in topics_df.columns:
        result = result.merge(
            topics_df[["_id", "category"]],
            left_on="topic_id",
            right_on="_id",
            how="left"
        )
        result = result.drop(columns=["_id"])
    
    # Drop the topicId column if it exists
    if "topicId" in result.columns:
        result = result.drop(columns=["topicId"])
    
    # Sort by subscriber count descending
    result = result.sort_values("subscriber_count", ascending=False).reset_index(drop=True)
    
    logger.info(f"Calculated subscriber counts for {len(result)} topics")
    
    return result


def calculate_media_support_scores(
    evaluations_df: pd.DataFrame,
    issues_df: pd.DataFrame,
    media_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate cumulative support scores for media sources based on user evaluations.
    
    Logic:
    1. When a user agrees with a specific perspective (left/center/right) on an issue
    2. Find all media sources that covered that issue with the same perspective
    3. Attribute +1 support to those media sources
    4. Calculate cumulative support over time
    
    Args:
        evaluations_df: DataFrame with user issue evaluations (from load_issue_evaluations)
        issues_df: DataFrame with issue information (from load_issues)
        media_df: DataFrame with media source information (from load_media_sources)
        
    Returns:
        DataFrame with columns:
            - media_id: str
            - media_name: str
            - date: datetime
            - perspective: str (left, center, right)
            - support_count: int (support on that date)
            - cumulative_support: int (cumulative support up to that date)
    """
    if evaluations_df.empty or issues_df.empty:
        logger.warning("Empty evaluations or issues dataframe provided")
        return pd.DataFrame()
    
    # Validate required columns
    if "issueId" not in evaluations_df.columns or "perspective" not in evaluations_df.columns:
        logger.error("Required columns missing in evaluations dataframe")
        return pd.DataFrame()
    
    if "evaluatedAt" not in evaluations_df.columns:
        logger.error("evaluatedAt column missing in evaluations dataframe")
        return pd.DataFrame()
    
    # Prepare issues data with sources
    issues_with_sources = []
    for _, issue in issues_df.iterrows():
        issue_id = issue.get("_id")
        sources = issue.get("sources", [])
        
        if not sources or not isinstance(sources, list):
            continue
        
        for source in sources:
            if isinstance(source, dict):
                issues_with_sources.append({
                    "issue_id": str(issue_id),
                    "media_id": source.get("_id"),
                    "media_name": source.get("name"),
                    "media_perspective": source.get("perspective")
                })
    
    if not issues_with_sources:
        logger.warning("No issue sources found")
        return pd.DataFrame()
    
    issues_sources_df = pd.DataFrame(issues_with_sources)
    
    # Merge evaluations with issue sources
    # Match when user's perspective matches media's perspective
    merged = evaluations_df.merge(
        issues_sources_df,
        left_on="issueId",
        right_on="issue_id",
        how="inner"
    )
    
    # Map perspectives to match
    # User perspective: left, center, right
    # Media perspective: left, center_left, center, center_right, right
    # Mapping: left -> left, center_left
    #          center -> center
    #          right -> center_right, right
    
    def perspectives_match(user_perspective, media_perspective):
        if user_perspective == "left":
            return media_perspective in ["left", "center_left"]
        elif user_perspective == "center":
            return media_perspective == "center"
        elif user_perspective == "right":
            return media_perspective in ["center_right", "right"]
        return False
    
    merged["match"] = merged.apply(
        lambda row: perspectives_match(row["perspective"], row["media_perspective"]),
        axis=1
    )
    
    # Filter only matching evaluations
    matched = merged[merged["match"]].copy()
    
    if matched.empty:
        logger.warning("No matching evaluations found")
        return pd.DataFrame()
    
    # Extract date from evaluatedAt
    matched["date"] = matched["evaluatedAt"].dt.date
    matched["date"] = pd.to_datetime(matched["date"])
    
    # Count support per media per date per perspective
    support_counts = matched.groupby(
        ["media_id", "media_name", "date", "perspective"]
    ).size().to_frame(name="support_count").reset_index()
    
    # Sort by media and date
    support_counts = support_counts.sort_values(["media_id", "perspective", "date"])
    
    # Calculate cumulative support for each media and perspective
    support_counts["cumulative_support"] = support_counts.groupby(
        ["media_id", "perspective"]
    )["support_count"].cumsum()
    
    logger.info(f"Calculated support scores for {support_counts['media_id'].nunique()} media sources")
    
    return support_counts


def get_recent_issues(
    issues_df: pd.DataFrame,
    limit: int = 20
) -> pd.DataFrame:
    """
    Get most recent issues sorted by creation date.
    
    Args:
        issues_df: DataFrame with issue information (from load_issues)
        limit: Maximum number of issues to return
        
    Returns:
        DataFrame with recent issues, sorted by createdAt descending
    """
    if issues_df.empty:
        logger.warning("Empty issues dataframe provided")
        return pd.DataFrame()
    
    # Check if createdAt column exists
    if "createdAt" not in issues_df.columns:
        logger.warning("createdAt column not found in issues dataframe")
        return issues_df.head(limit)
    
    # Sort by createdAt descending and take top N
    recent = issues_df.sort_values("createdAt", ascending=False).head(limit).copy()
    
    logger.info(f"Retrieved {len(recent)} recent issues")
    
    return recent
