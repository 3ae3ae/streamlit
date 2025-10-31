"""
Chart generation module for MongoDB visualization tool.
Handles creation of interactive Plotly charts with consistent theming.
"""

import logging
from typing import Optional

import pandas as pd
import plotly.graph_objects as go

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Color palette for political perspectives (optimized for dark mode)
COLORS = {
    "left": "#FF6B6B",           # Brighter red for left/progressive
    "center_left": "#FFA94D",    # Brighter orange for center-left
    "center": "#4DABF7",         # Brighter blue for center
    "center_right": "#CC5DE8",   # Brighter purple for center-right
    "right": "#51CF66",          # Brighter green for right/conservative
    "unknown": "#ADB5BD"         # Lighter gray for unknown/empty
}

# Chart theme configuration
CHART_THEME = {
    "font_family": "Malgun Gothic, Apple SD Gothic Neo, sans-serif",
    "font_size": 12,
    "title_font_size": 16,
    "background_color": "rgba(0,0,0,0)",  # Transparent to adapt to theme
    "paper_color": "rgba(0,0,0,0)",  # Transparent to adapt to theme
    "grid_color": "#444444",  # Darker grid for better visibility in both modes
    "text_color": "#212529",  # Darker text for readability on light backgrounds
    "height": 500
}


def calculate_optimal_y_range(data: pd.Series) -> tuple[float, float]:
    """
    Calculate optimal y-axis range based on data variance with padding.
    
    This function computes the min and max values from the data and adds
    10% padding to ensure small changes are visible and the chart doesn't
    feel cramped.
    
    Args:
        data: Pandas Series containing numeric data
        
    Returns:
        Tuple of (y_min, y_max) for the y-axis range
    """
    if data.empty or data.isna().all():
        # Return default range if no valid data
        return (0, 100)
    
    # Get min and max values, ignoring NaN
    min_val = data.min()
    max_val = data.max()
    
    # Calculate data range
    data_range = max_val - min_val
    
    # Add 10% padding for better visibility
    # If data_range is 0 (all values are the same), use a small default padding
    if data_range == 0:
        padding = max(abs(min_val) * 0.1, 1)  # 10% of value or minimum 1
    else:
        padding = data_range * 0.1
    
    y_min = min_val - padding
    y_max = max_val + padding
    
    return (y_min, y_max)


def apply_chart_theme(fig: go.Figure, title: Optional[str] = None) -> go.Figure:
    """
    Apply consistent theme to all charts.
    
    This function applies a unified visual style including fonts, colors,
    and layout settings to ensure all charts have a professional and
    consistent appearance. Supports both light and dark modes.
    
    Args:
        fig: Plotly figure object to style
        title: Optional chart title
        
    Returns:
        Styled Plotly figure
    """
    fig.update_layout(
        font=dict(
            family=CHART_THEME["font_family"],
            size=CHART_THEME["font_size"],
            color=CHART_THEME["text_color"]
        ),
        title=dict(
            text=title,
            font=dict(
                size=CHART_THEME["title_font_size"],
                color=CHART_THEME["text_color"]
            ),
            x=0.5,
            xanchor="center"
        ) if title else None,
        plot_bgcolor=CHART_THEME["background_color"],
        paper_bgcolor=CHART_THEME["paper_color"],
        height=CHART_THEME["height"],
        hovermode="closest",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(color=CHART_THEME["text_color"])
        )
    )
    
    # Update axes styling with light text for dark mode
    fig.update_xaxes(
        gridcolor=CHART_THEME["grid_color"],
        showline=True,
        linewidth=1,
        linecolor=CHART_THEME["grid_color"],
        color=CHART_THEME["text_color"]
    )
    
    fig.update_yaxes(
        gridcolor=CHART_THEME["grid_color"],
        showline=True,
        linewidth=1,
        linecolor=CHART_THEME["grid_color"],
        color=CHART_THEME["text_color"]
    )
    
    return fig



def create_political_preference_pie_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create pie chart showing distribution of political preferences across all users.
    
    Args:
        df: DataFrame with user data including 'politicalPreference' column
        
    Returns:
        Plotly figure with pie chart
    """
    if df.empty:
        logger.warning("Empty dataframe provided for pie chart")
        fig = go.Figure()
        fig.add_annotation(
            text="데이터가 없습니다",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        return apply_chart_theme(fig, "전체 사용자 정치 성향 분포")
    
    # Count political preferences, handling empty/null values
    if "politicalPreference" not in df.columns:
        logger.error("politicalPreference column not found")
        fig = go.Figure()
        return apply_chart_theme(fig, "전체 사용자 정치 성향 분포")
    
    # Fill NaN values with 'unknown'
    preference_counts = df["politicalPreference"].fillna("unknown").value_counts()
    
    # Map preferences to Korean labels
    label_map = {
        "left": "진보",
        "center_left": "중도진보",
        "center": "중도",
        "center_right": "중도보수",
        "right": "보수",
        "unknown": "미분류"
    }
    
    labels = [label_map.get(pref, pref) for pref in preference_counts.index]
    values = preference_counts.values
    colors = [COLORS.get(pref, COLORS["unknown"]) for pref in preference_counts.index]
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hovertemplate="<b>%{label}</b><br>" +
                      "사용자 수: %{value}<br>" +
                      "비율: %{percent}<br>" +
                      "<extra></extra>",
        textinfo="label+percent",
        textposition="auto"
    )])
    
    return apply_chart_theme(fig, "전체 사용자 정치 성향 분포")


def create_time_series_chart(
    df: pd.DataFrame,
    date_range: str,
    view_type: str,
    category: Optional[str] = None
) -> go.Figure:
    """
    Create time-series chart for political score changes over time.
    
    Args:
        df: DataFrame with aggregated political scores by date and category
        date_range: '7d' or '30d' for date range filter
        view_type: 'category' for category-specific view or 'average' for overall average
        category: Specific category to display (required if view_type is 'category')
        
    Returns:
        Plotly figure with time-series chart
    """
    if df.empty:
        logger.warning("Empty dataframe provided for time series chart")
        fig = go.Figure()
        fig.add_annotation(
            text="데이터가 없습니다",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        return apply_chart_theme(fig, "시간별 활성 유저 변화")
    
    # Category name mapping
    category_map = {
        "politics": "정치",
        "economy": "경제",
        "society": "사회",
        "culture": "문화",
        "technology": "기술",
        "international": "국제"
    }
    
    fig = go.Figure()
    
    if view_type == "category" and category:
        # Show specific category
        category_data = df[df["category"] == category].copy()
        
        if category_data.empty:
            fig.add_annotation(
                text=f"{category_map.get(category, category)} 카테고리 데이터가 없습니다",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=16)
            )
            return apply_chart_theme(fig, f"{category_map.get(category, category)} - 시간별 활성 유저 변화")
        
        # Sort by date
        category_data = category_data.sort_values("date")
        
        # Add traces for left, center, right proportions
        fig.add_trace(go.Scatter(
            x=category_data["date"],
            y=category_data["left_proportion"] * 100,
            mode="lines+markers",
            name="진보",
            line=dict(color=COLORS["left"], width=2),
            marker=dict(size=6),
            hovertemplate="<b>진보</b><br>" +
                          "날짜: %{x|%Y-%m-%d}<br>" +
                          "비율: %{y:.1f}%<br>" +
                          "<extra></extra>"
        ))
        
        fig.add_trace(go.Scatter(
            x=category_data["date"],
            y=category_data["center_proportion"] * 100,
            mode="lines+markers",
            name="중도",
            line=dict(color=COLORS["center"], width=2),
            marker=dict(size=6),
            hovertemplate="<b>중도</b><br>" +
                          "날짜: %{x|%Y-%m-%d}<br>" +
                          "비율: %{y:.1f}%<br>" +
                          "<extra></extra>"
        ))
        
        fig.add_trace(go.Scatter(
            x=category_data["date"],
            y=category_data["right_proportion"] * 100,
            mode="lines+markers",
            name="보수",
            line=dict(color=COLORS["right"], width=2),
            marker=dict(size=6),
            hovertemplate="<b>보수</b><br>" +
                          "날짜: %{x|%Y-%m-%d}<br>" +
                          "비율: %{y:.1f}%<br>" +
                          "<extra></extra>"
        ))
        
        title = f"{category_map.get(category, category)} - 시간별 활성 유저 변화"
        
    else:
        # Show average across all categories
        # Calculate average proportions across categories for each date
        avg_data = df.groupby("date").agg({
            "left_proportion": "mean",
            "center_proportion": "mean",
            "right_proportion": "mean"
        }).reset_index()
        
        avg_data = avg_data.sort_values("date")
        
        fig.add_trace(go.Scatter(
            x=avg_data["date"],
            y=avg_data["left_proportion"] * 100,
            mode="lines+markers",
            name="진보 (평균)",
            line=dict(color=COLORS["left"], width=2),
            marker=dict(size=6),
            hovertemplate="<b>진보 (평균)</b><br>" +
                          "날짜: %{x|%Y-%m-%d}<br>" +
                          "비율: %{y:.1f}%<br>" +
                          "<extra></extra>"
        ))
        
        fig.add_trace(go.Scatter(
            x=avg_data["date"],
            y=avg_data["center_proportion"] * 100,
            mode="lines+markers",
            name="중도 (평균)",
            line=dict(color=COLORS["center"], width=2),
            marker=dict(size=6),
            hovertemplate="<b>중도 (평균)</b><br>" +
                          "날짜: %{x|%Y-%m-%d}<br>" +
                          "비율: %{y:.1f}%<br>" +
                          "<extra></extra>"
        ))
        
        fig.add_trace(go.Scatter(
            x=avg_data["date"],
            y=avg_data["right_proportion"] * 100,
            mode="lines+markers",
            name="보수 (평균)",
            line=dict(color=COLORS["right"], width=2),
            marker=dict(size=6),
            hovertemplate="<b>보수 (평균)</b><br>" +
                          "날짜: %{x|%Y-%m-%d}<br>" +
                          "비율: %{y:.1f}%<br>" +
                          "<extra></extra>"
        ))
        
        title = "전체 카테고리 평균 - 시간별 활성 유저 변화"
    
    # Update layout with zoom and pan enabled
    fig.update_xaxes(
        title="날짜",
        type="date"
    )
    
    # Calculate optimal y-axis range based on data
    if view_type == "category" and category:
        category_data = df[df["category"] == category].copy()
        if not category_data.empty:
            # Combine all proportion data for range calculation
            all_proportions = pd.concat([
                category_data["left_proportion"] * 100,
                category_data["center_proportion"] * 100,
                category_data["right_proportion"] * 100
            ], ignore_index=True)
            y_min, y_max = calculate_optimal_y_range(all_proportions)
        else:
            y_min, y_max = 0, 100
    else:
        # Average view
        avg_data = df.groupby("date").agg({
            "left_proportion": "mean",
            "center_proportion": "mean",
            "right_proportion": "mean"
        }).reset_index()
        
        if not avg_data.empty:
            all_proportions = pd.concat([
                avg_data["left_proportion"] * 100,
                avg_data["center_proportion"] * 100,
                avg_data["right_proportion"] * 100
            ], ignore_index=True)
            y_min, y_max = calculate_optimal_y_range(all_proportions)
        else:
            y_min, y_max = 0, 100
    
    fig.update_yaxes(
        title="비율 (%)",
        range=[y_min, y_max],
        fixedrange=False  # Allow manual adjustment
    )
    
    # Enable zoom and pan
    fig.update_layout(
        dragmode="zoom",
        hovermode="x unified"
    )
    
    return apply_chart_theme(fig, title)


def create_time_series_pie_animation(
    df: pd.DataFrame,
    view_type: str,
    category: Optional[str] = None
) -> go.Figure:
    """Create animated pie chart showing political preference distribution over time."""
    if df.empty:
        logger.warning("Empty dataframe provided for time series pie chart")
        fig = go.Figure()
        fig.add_annotation(
            text="데이터가 없습니다",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        fig = apply_chart_theme(fig)
        fig.update_layout(
            title=dict(
                text="시간별 활성 유저 분포 (원그래프)",
                font=dict(
                    size=CHART_THEME["title_font_size"],
                    color=CHART_THEME["text_color"]
                ),
                x=0.5,
                xanchor="center"
            )
        )
        return fig

    category_map = {
        "politics": "정치",
        "economy": "경제",
        "society": "사회",
        "culture": "문화",
        "technology": "기술",
        "international": "국제"
    }

    labels = ["진보", "중도", "보수"]
    colors = [COLORS["left"], COLORS["center"], COLORS["right"]]

    if view_type == "category" and category:
        animation_df = df[df["category"] == category].copy()
        if animation_df.empty:
            fig = go.Figure()
            fig.add_annotation(
                text=f"{category_map.get(category, category)} 카테고리 데이터가 없습니다",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=16)
            )
            fig = apply_chart_theme(fig)
            fig.update_layout(
                title=dict(
                    text=f"{category_map.get(category, category)} - 시간별 활성 유저 분포",
                    font=dict(
                        size=CHART_THEME["title_font_size"],
                        color=CHART_THEME["text_color"]
                    ),
                    x=0.5,
                    xanchor="center"
                )
            )
            return fig

        animation_df = animation_df.sort_values("date")
        animation_df["label"] = animation_df["date"].dt.strftime("%Y-%m-%d")
        animation_df["left_value"] = animation_df["left_proportion"].fillna(0) * 100
        animation_df["center_value"] = animation_df["center_proportion"].fillna(0) * 100
        animation_df["right_value"] = animation_df["right_proportion"].fillna(0) * 100
        title_prefix = f"{category_map.get(category, category)} - 시간별 활성 유저 분포"
    else:
        animation_df = (
            df.groupby("date").agg({
                "left_proportion": "mean",
                "center_proportion": "mean",
                "right_proportion": "mean"
            }).reset_index()
        )

        if animation_df.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="표시할 데이터가 없습니다",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=16)
            )
            fig = apply_chart_theme(fig)
            fig.update_layout(
                title=dict(
                    text="전체 카테고리 평균 - 시간별 활성 유저 분포",
                    font=dict(
                        size=CHART_THEME["title_font_size"],
                        color=CHART_THEME["text_color"]
                    ),
                    x=0.5,
                    xanchor="center"
                )
            )
            return fig

        animation_df = animation_df.sort_values("date")
        animation_df["label"] = animation_df["date"].dt.strftime("%Y-%m-%d")
        animation_df["left_value"] = animation_df["left_proportion"].fillna(0) * 100
        animation_df["center_value"] = animation_df["center_proportion"].fillna(0) * 100
        animation_df["right_value"] = animation_df["right_proportion"].fillna(0) * 100
        title_prefix = "전체 카테고리 평균 - 시간별 활성 유저 분포"

    first_row = animation_df.iloc[0]

    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=labels,
        values=[first_row["left_value"], first_row["center_value"], first_row["right_value"]],
        marker=dict(
            colors=colors,
            line=dict(color="rgba(255,255,255,0.15)", width=2)
        ),
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>비율: %{value:.1f}%<br><extra></extra>",
        hole=0.35,
        sort=False
    ))

    frame_duration = 900  # milliseconds per frame
    transition_duration = 500  # easing duration between frames
    easing_function = "cubic-in-out"

    frames = []
    for _, row in animation_df.iterrows():
        frame_name = row["label"]
        frames.append(go.Frame(
            data=[go.Pie(
                labels=labels,
                values=[row["left_value"], row["center_value"], row["right_value"]],
                marker=dict(
                    colors=colors,
                    line=dict(color="rgba(255,255,255,0.15)", width=2)
                ),
                textinfo="label+percent",
                hovertemplate="<b>%{label}</b><br>비율: %{value:.1f}%<br><extra></extra>",
                hole=0.35,
                sort=False
            )],
            name=frame_name,
            layout=go.Layout(
                title=dict(
                    text=f"{title_prefix} - {frame_name}",
                    font=dict(
                        size=CHART_THEME["title_font_size"],
                        color=CHART_THEME["text_color"]
                    ),
                    x=0.5,
                    xanchor="center"
                ),
                transition=dict(duration=transition_duration, easing=easing_function)
            )
        ))

    fig.frames = frames

    slider_steps = []
    for frame in frames:
        slider_steps.append({
            "label": frame.name,
            "method": "animate",
            "args": [
                [frame.name],
                {
                    "frame": {"duration": frame_duration, "redraw": True},
                    "transition": {"duration": transition_duration, "easing": easing_function},
                    "mode": "immediate"
                }
            ]
        })

    fig = apply_chart_theme(fig)

    fig.update_layout(
        title=dict(
            text=f"{title_prefix} - {first_row['label']}",
            font=dict(
                size=CHART_THEME["title_font_size"],
                color=CHART_THEME["text_color"]
            ),
            x=0.5,
            xanchor="center"
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5
        ),
        updatemenus=[
            {
                "type": "buttons",
                "direction": "left",
                "pad": {"r": 10, "t": 70},
                "showactive": False,
                "x": 0.0,
                "y": 1.12,
                "buttons": [
                    {
                        "label": "▶ 재생",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": frame_duration, "redraw": True},
                                "fromcurrent": True,
                                "transition": {"duration": transition_duration, "easing": easing_function}
                            }
                        ]
                    },
                    {
                        "label": "⏸ 정지",
                        "method": "animate",
                        "args": [
                            [None],
                            {
                                "frame": {"duration": 0, "redraw": False},
                                "mode": "immediate",
                                "transition": {"duration": 0, "easing": easing_function}
                            }
                        ]
                    }
                ]
            }
        ],
        sliders=[
            {
                "active": 0,
                "y": -0.1,
                "x": 0.1,
                "len": 0.8,
                "pad": {"t": 50, "b": 10},
                "currentvalue": {
                    "prefix": "날짜: ",
                    "visible": True,
                    "font": {
                        "size": 12,
                        "color": CHART_THEME["text_color"]
                    }
                },
                "steps": slider_steps
            }
        ]
    )

    fig.update_traces(
        sort=False,
        hole=0.35,
        marker=dict(
            colors=colors,
            line=dict(color="rgba(255,255,255,0.15)", width=2)
        ),
        textfont=dict(size=13)
    )

    return fig


def create_user_political_journey_chart(
    df: pd.DataFrame,
    user_id: str
) -> go.Figure:
    """
    Create chart showing individual user's political score history across all categories.
    
    Args:
        df: DataFrame with political score history
        user_id: User ID to display
        
    Returns:
        Plotly figure with user's political journey
    """
    if df.empty:
        logger.warning("Empty dataframe provided for user journey chart")
        fig = go.Figure()
        fig.add_annotation(
            text="데이터가 없습니다",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        return apply_chart_theme(fig, f"사용자 {user_id} 정치 성향 변화")
    
    # Filter data for specific user
    user_data = df[df["userId"] == user_id].copy()
    
    if user_data.empty:
        logger.warning(f"No data found for user {user_id}")
        fig = go.Figure()
        fig.add_annotation(
            text=f"사용자 ID '{user_id}'에 대한 데이터를 찾을 수 없습니다",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        return apply_chart_theme(fig, f"사용자 {user_id} 정치 성향 변화")
    
    # Sort by date
    user_data = user_data.sort_values("createdAt")
    
    # Category name mapping
    category_map = {
        "politics": "정치",
        "economy": "경제",
        "society": "사회",
        "culture": "문화",
        "technology": "기술",
        "international": "국제"
    }
    
    # Category colors (optimized for dark mode)
    category_colors = {
        "politics": "#FF6B6B",
        "economy": "#4DABF7",
        "society": "#51CF66",
        "culture": "#FFA94D",
        "technology": "#CC5DE8",
        "international": "#20C997"
    }
    
    fig = go.Figure()
    
    # Add traces for each category (showing left, center, right scores)
    categories = ["politics", "economy", "society", "culture", "technology", "international"]
    
    for cat in categories:
        left_col = f"{cat}_left"
        right_col = f"{cat}_right"
        
        if left_col not in user_data.columns:
            continue
        
        # Calculate net score (left - right, with center as neutral)
        # Positive = more left-leaning, Negative = more right-leaning
        user_data[f"{cat}_net_score"] = user_data[left_col] - user_data[right_col]
        
        fig.add_trace(go.Scatter(
            x=user_data["createdAt"],
            y=user_data[f"{cat}_net_score"],
            mode="lines+markers",
            name=category_map.get(cat, cat),
            line=dict(color=category_colors.get(cat, "#95A5A6"), width=2),
            marker=dict(size=6),
            hovertemplate=f"<b>{category_map.get(cat, cat)}</b><br>" +
                          "날짜: %{x|%Y-%m-%d}<br>" +
                          "진보-보수 점수: %{y:.1f}<br>" +
                          "<extra></extra>"
        ))
    
    # Add horizontal line at y=0 (neutral)
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="gray",
        annotation_text="중립",
        annotation_position="right"
    )
    
    # Update layout
    fig.update_xaxes(
        title="날짜",
        type="date"
    )
    
    # Calculate optimal y-axis range based on all net scores
    all_net_scores = []
    for cat in categories:
        net_score_col = f"{cat}_net_score"
        if net_score_col in user_data.columns:
            all_net_scores.extend(user_data[net_score_col].dropna().tolist())
    
    if all_net_scores:
        net_scores_series = pd.Series(all_net_scores)
        y_min, y_max = calculate_optimal_y_range(net_scores_series)
        # Ensure the range includes 0 (neutral line)
        y_min = min(y_min, 0)
        y_max = max(y_max, 0)
    else:
        y_min, y_max = -100, 100
    
    fig.update_yaxes(
        title="정치 성향 점수 (진보 ← 0 → 보수)",
        range=[y_min, y_max],
        fixedrange=False  # Allow manual adjustment
    )
    
    # Enable zoom and pan
    fig.update_layout(
        dragmode="zoom",
        hovermode="x unified"
    )
    
    return apply_chart_theme(fig, f"사용자 {user_id} 정치 성향 변화")



def create_media_support_chart(
    df: pd.DataFrame,
    media_id: Optional[str] = None,
    media_ids: Optional[list] = None
) -> go.Figure:
    """
    Create cumulative support chart for one or multiple media sources.
    
    Args:
        df: DataFrame with media support scores over time
        media_id: Single media source ID to display (for backward compatibility)
        media_ids: List of media source IDs to display (for multi-media comparison)
        
    Returns:
        Plotly figure with cumulative support chart
    """
    if df.empty:
        logger.warning("Empty dataframe provided for media support chart")
        fig = go.Figure()
        fig.add_annotation(
            text="데이터가 없습니다",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        return apply_chart_theme(fig, "언론사 지지도")
    
    # Determine which media sources to display
    if media_ids is not None and len(media_ids) > 0:
        # Multi-media comparison mode
        selected_media_ids = media_ids
        is_multi_mode = True
    elif media_id is not None:
        # Single media mode (backward compatibility)
        selected_media_ids = [media_id]
        is_multi_mode = False
    else:
        logger.error("Either media_id or media_ids must be provided")
        fig = go.Figure()
        fig.add_annotation(
            text="언론사를 선택해주세요",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        return apply_chart_theme(fig, "언론사 지지도")
    
    # Filter data for selected media sources
    media_data = df[df["media_id"].isin(selected_media_ids)].copy()
    
    if media_data.empty:
        logger.warning(f"No data found for selected media sources")
        fig = go.Figure()
        fig.add_annotation(
            text="선택한 언론사에 대한 데이터를 찾을 수 없습니다",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        return apply_chart_theme(fig, "언론사 지지도")
    
    # Sort by date
    media_data = media_data.sort_values("date")
    
    # Perspective mapping
    perspective_map = {
        "left": "진보",
        "center": "중도",
        "right": "보수"
    }
    
    # Color palette for multiple media sources (optimized for dark mode)
    # Use distinct bright colors for each media source
    media_colors = [
        "#FF6B6B",  # Bright Red
        "#4DABF7",  # Bright Blue
        "#51CF66",  # Bright Green
        "#FFA94D",  # Bright Orange
        "#CC5DE8",  # Bright Purple
        "#20C997",  # Bright Turquoise
        "#FF922B",  # Bright Carrot
    ]
    
    fig = go.Figure()
    
    if is_multi_mode:
        # Multi-media comparison: one line per media source (aggregate perspectives)
        for idx, selected_id in enumerate(selected_media_ids):
            media_subset = media_data[media_data["media_id"] == selected_id]
            
            if media_subset.empty:
                continue
            
            # Get media name
            media_name = media_subset["media_name"].iloc[0] if "media_name" in media_subset.columns else selected_id
            
            # Aggregate all perspectives for this media (sum cumulative support across perspectives)
            # Group by date and sum cumulative support
            aggregated = media_subset.groupby("date").agg({
                "cumulative_support": "sum"
            }).reset_index()
            
            aggregated = aggregated.sort_values("date")
            
            # Use distinct color for each media
            color = media_colors[idx % len(media_colors)]
            
            fig.add_trace(go.Scatter(
                x=aggregated["date"],
                y=aggregated["cumulative_support"],
                mode="lines+markers",
                name=media_name,
                line=dict(color=color, width=2),
                marker=dict(size=6),
                hovertemplate=f"<b>{media_name}</b><br>" +
                              "날짜: %{x|%Y-%m-%d}<br>" +
                              "총 누적 지지도: %{y}<br>" +
                              "<extra></extra>"
            ))
        
        title = f"언론사 비교 ({len(selected_media_ids)}개)"
        
    else:
        # Single media mode: show perspectives separately
        media_name = media_data["media_name"].iloc[0] if "media_name" in media_data.columns else media_id
        
        # Add traces for each perspective
        for perspective in ["left", "center", "right"]:
            perspective_data = media_data[media_data["perspective"] == perspective]
            
            if not perspective_data.empty:
                fig.add_trace(go.Scatter(
                    x=perspective_data["date"],
                    y=perspective_data["cumulative_support"],
                    mode="lines+markers",
                    name=perspective_map.get(perspective, perspective),
                    line=dict(color=COLORS.get(perspective, "#95A5A6"), width=2),
                    marker=dict(size=6),
                    hovertemplate=f"<b>{perspective_map.get(perspective, perspective)}</b><br>" +
                                  "날짜: %{x|%Y-%m-%d}<br>" +
                                  "누적 지지도: %{y}<br>" +
                                  "<extra></extra>"
                ))
        
        title = f"{media_name} - 누적 지지도"
    
    # Update layout
    fig.update_xaxes(
        title="날짜",
        type="date"
    )
    
    # Calculate optimal y-axis range based on cumulative support data
    all_support_values = media_data["cumulative_support"].dropna()
    if not all_support_values.empty:
        y_min, y_max = calculate_optimal_y_range(all_support_values)
        # Ensure y_min is at least 0 for cumulative data
        y_min = max(0, y_min)
    else:
        y_min, y_max = 0, 100
    
    fig.update_yaxes(
        title="누적 지지도",
        range=[y_min, y_max],
        fixedrange=False  # Allow manual adjustment
    )
    
    # Enable zoom and pan
    fig.update_layout(
        dragmode="zoom",
        hovermode="x unified"
    )
    
    return apply_chart_theme(fig, title)


def create_issue_evaluation_pie_chart(
    df: pd.DataFrame,
    issue_id: str
) -> go.Figure:
    """
    Create pie chart showing distribution of user evaluations for a specific issue.
    
    Args:
        df: DataFrame with issue evaluation data
        issue_id: Issue ID to display
        
    Returns:
        Plotly figure with pie chart
    """
    if df.empty:
        logger.warning("Empty dataframe provided for issue evaluation chart")
        fig = go.Figure()
        fig.add_annotation(
            text="데이터가 없습니다",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        return apply_chart_theme(fig, "이슈 평가 분포")
    
    # Filter data for specific issue
    issue_data = df[df["issueId"] == issue_id].copy()
    
    if issue_data.empty:
        logger.warning(f"No evaluation data found for issue {issue_id}")
        fig = go.Figure()
        fig.add_annotation(
            text=f"이슈 ID '{issue_id}'에 대한 평가 데이터를 찾을 수 없습니다",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        return apply_chart_theme(fig, "이슈 평가 분포")
    
    # Count perspectives
    if "perspective" not in issue_data.columns:
        logger.error("perspective column not found")
        fig = go.Figure()
        return apply_chart_theme(fig, "이슈 평가 분포")
    
    perspective_counts = issue_data["perspective"].value_counts()
    
    # Perspective mapping
    perspective_map = {
        "left": "진보",
        "center": "중도",
        "right": "보수"
    }
    
    labels = [perspective_map.get(p, p) for p in perspective_counts.index]
    values = perspective_counts.values
    colors = [COLORS.get(p, COLORS["unknown"]) for p in perspective_counts.index]
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hovertemplate="<b>%{label}</b><br>" +
                      "평가 수: %{value}<br>" +
                      "비율: %{percent}<br>" +
                      "<extra></extra>",
        textinfo="label+percent",
        textposition="auto"
    )])
    
    return apply_chart_theme(fig, f"이슈 {issue_id} - 평가 분포")
