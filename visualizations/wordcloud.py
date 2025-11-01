"""
Word cloud generation module for MongoDB visualization tool.
Handles creation of word clouds for topic visualization based on subscriber counts.
"""

import logging
from typing import Optional

import pandas as pd
from PIL import Image
from wordcloud import WordCloud

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_topic_wordcloud(
    topics_df: pd.DataFrame,
    subscriptions_df: pd.DataFrame,
    top_n: int = 50,
    width: int = 800,
    height: int = 400,
    background_color: str = "white",
    colormap: str = "viridis"
) -> Optional[Image.Image]:
    """
    Generate word cloud for top N topics by subscriber count.
    
    This function creates a word cloud visualization where:
    - Word size is proportional to the number of subscribers
    - Only the top N topics by subscriber count are included
    - Korean text is properly rendered with appropriate font
    
    Args:
        topics_df: DataFrame with topic information (from load_topics)
                   Expected columns: _id, name
        subscriptions_df: DataFrame with user topic subscriptions (from load_topic_subscriptions)
                         Expected columns: topicId
        top_n: Number of top topics to include in the word cloud (default: 50)
        width: Width of the word cloud image in pixels (default: 800)
        height: Height of the word cloud image in pixels (default: 400)
        background_color: Background color of the word cloud (default: "white")
        colormap: Matplotlib colormap to use for word colors (default: "viridis")
        
    Returns:
        PIL Image object containing the word cloud, or None if generation fails
        
    Example:
        >>> topics = load_topics()
        >>> subscriptions = load_topic_subscriptions()
        >>> wordcloud_image = create_topic_wordcloud(topics, subscriptions, top_n=30)
        >>> if wordcloud_image:
        >>>     st.image(wordcloud_image)
    """
    if topics_df.empty:
        logger.warning("Empty topics dataframe provided")
        return None
    
    if subscriptions_df.empty:
        logger.warning("Empty subscriptions dataframe provided - no subscriber data")
        # Could still generate with zero counts, but not very useful
        return None
    
    try:
        # Import aggregator function to calculate subscriber counts
        from processing.aggregators import calculate_topic_subscriber_counts
        
        # Calculate subscriber counts for all topics
        topic_counts = calculate_topic_subscriber_counts(topics_df, subscriptions_df)
        
        if topic_counts.empty:
            logger.warning("No topic counts calculated")
            return None
        
        # Filter to top N topics
        top_topics = topic_counts.head(top_n)
        
        if top_topics.empty or top_topics["subscriber_count"].sum() == 0:
            logger.warning("No topics with subscribers found")
            return None
        
        # Create frequency dictionary for word cloud
        # Format: {word: frequency}
        word_frequencies = {}
        for _, row in top_topics.iterrows():
            topic_name = str(row["topic_name"]) if pd.notna(row["topic_name"]) else ""
            subscriber_count = int(row["subscriber_count"]) if pd.notna(row["subscriber_count"]) else 0
            
            if topic_name and subscriber_count > 0:
                word_frequencies[topic_name] = subscriber_count
        
        if not word_frequencies:
            logger.warning("No valid word frequencies generated")
            return None
        
        logger.info(f"Generating word cloud with {len(word_frequencies)} topics")
        
        # Configure word cloud with Korean font support
        # Try to find a Korean font on the system
        font_path = _get_korean_font_path()
        
        # Create word cloud
        wc_params = {
            "width": width,
            "height": height,
            "background_color": background_color,
            "colormap": colormap,
            "min_font_size": 10,
            "max_words": top_n,
            "prefer_horizontal": 0.7,  # 70% horizontal words
            "margin": 10
        }
        
        # Add font_path only if available
        if font_path:
            wc_params["font_path"] = font_path
        
        wordcloud = WordCloud(**wc_params).generate_from_frequencies(word_frequencies)
        
        # Convert to PIL Image
        image = wordcloud.to_image()
        
        logger.info("Word cloud generated successfully")
        return image
        
    except Exception as e:
        logger.error(f"Error generating word cloud: {e}", exc_info=True)
        return None


def create_keyword_wordcloud(
    keyword_df: pd.DataFrame,
    word_column: str = "keyword",
    value_column: str = "watch_total",
    max_words: int = 80,
    width: int = 800,
    height: int = 400,
    background_color: str = "white",
    colormap: str = "viridis"
) -> Optional[Image.Image]:
    """
    Generate a word cloud from keyword frequency data.
    
    Args:
        keyword_df: DataFrame containing keyword frequencies
        word_column: Column name containing keyword text
        value_column: Column name containing numeric weight
        max_words: Maximum number of keywords to render
        width: Width of the resulting image
        height: Height of the resulting image
        background_color: Background color for the word cloud
        colormap: Matplotlib colormap for word colors
    
    Returns:
        PIL Image object with the word cloud, or None if generation fails
    """
    if keyword_df.empty:
        logger.warning("Empty keyword dataframe provided; cannot generate word cloud")
        return None
    
    if word_column not in keyword_df.columns or value_column not in keyword_df.columns:
        logger.warning("Keyword dataframe missing required columns for word cloud generation")
        return None
    
    filtered = keyword_df[[word_column, value_column]].dropna()
    if filtered.empty:
        logger.warning("Keyword dataframe has no valid entries after dropping NaNs")
        return None
    
    filtered = filtered[filtered[value_column] > 0]
    if filtered.empty:
        logger.warning("Keyword dataframe has no positive weights for word cloud generation")
        return None
    
    filtered = filtered.sort_values(value_column, ascending=False).head(max_words)
    
    frequencies = {
        str(row[word_column]): float(row[value_column])
        for _, row in filtered.iterrows()
        if str(row[word_column]).strip()
    }
    
    if not frequencies:
        logger.warning("No keyword frequencies available after processing")
        return None
    
    try:
        font_path = _get_korean_font_path()
        
        wc_params = {
            "width": width,
            "height": height,
            "background_color": background_color,
            "colormap": colormap,
            "max_words": max_words,
            "prefer_horizontal": 0.7,
            "margin": 10
        }
        if font_path:
            wc_params["font_path"] = font_path
        
        wordcloud = WordCloud(**wc_params).generate_from_frequencies(frequencies)
        return wordcloud.to_image()
    except Exception as e:
        logger.error(f"Error generating keyword word cloud: {e}", exc_info=True)
        return None


def _get_korean_font_path() -> Optional[str]:
    """
    Attempt to find a Korean-compatible font on the system.
    
    Returns:
        Path to a Korean font file, or None if not found
    """
    import platform
    from pathlib import Path
    
    system = platform.system()
    
    # Common Korean font paths by operating system
    font_paths = []
    
    if system == "Darwin":  # macOS
        font_paths = [
            "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
            "/System/Library/Fonts/AppleSDGothicNeo.ttc",
            "/Library/Fonts/AppleGothic.ttf",
        ]
    elif system == "Linux":
        font_paths = [
            "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
            "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        ]
    elif system == "Windows":
        font_paths = [
            "C:\\Windows\\Fonts\\malgun.ttf",  # Malgun Gothic
            "C:\\Windows\\Fonts\\gulim.ttc",   # Gulim
        ]
    
    # Check each path
    for font_path in font_paths:
        if Path(font_path).exists():
            logger.info(f"Using Korean font: {font_path}")
            return font_path
    
    logger.warning("No Korean font found, word cloud may not display Korean text correctly")
    return None
