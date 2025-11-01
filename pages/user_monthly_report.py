"""
User monthly activity report page.

This page combines watch history, issue evaluations, political scores,
and media source metadata to highlight what a single user consumed and how
they behaved during the recent month.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

import pandas as pd
import streamlit as st

from data_loader import (
    load_issue_comments,
    load_issue_evaluations,
    load_issues,
    load_media_sources,
    load_political_score_history,
    load_user_comment_likes,
    load_user_watch_history
)
from processing.user_report import (
    build_comment_like_details,
    count_comment_likes_by_perspective,
    count_evaluations_by_perspective,
    count_user_watch_by_issue,
    count_watch_by_category,
    count_watch_by_day,
    filter_user_comment_likes,
    filter_user_issue_evaluations,
    filter_user_political_scores,
    get_user_recent_watch_history,
    summarize_media_perspectives
)
from visualizations.charts import (
    CATEGORY_LABELS,
    PERSPECTIVE_LABELS,
    create_media_perspective_distribution_chart,
    create_user_comment_like_distribution_chart,
    create_user_evaluation_distribution_chart,
    create_user_watch_daily_chart,
    create_user_political_journey_chart,
    create_user_watch_category_bar_chart
)

logger = logging.getLogger(__name__)

# Shared label mapping used for tabular presentation
CATEGORY_NAME_MAP = CATEGORY_LABELS

RECENT_WINDOW_DAYS = 30


def _prepare_recent_activity_summary(
    watch_df: pd.DataFrame,
    reference_date: datetime
) -> pd.DataFrame:
    """
    Compute aggregated recent watch activity across users for the selector.
    """
    if watch_df.empty or "watchedAt" not in watch_df.columns:
        return pd.DataFrame()
    
    recent_start = reference_date - timedelta(days=RECENT_WINDOW_DAYS)
    recent_watch = watch_df[
        (watch_df["watchedAt"] >= recent_start) &
        (watch_df["watchedAt"] <= reference_date)
    ]
    
    if recent_watch.empty:
        return pd.DataFrame()
    
    summary = (
        recent_watch.groupby("userId")
        .agg(
            last_watch=("watchedAt", "max"),
            watch_count=("issueId", "count"),
            issue_variety=("issueId", pd.Series.nunique)
        )
        .reset_index()
    )
    
    summary = summary.sort_values(
        ["watch_count", "last_watch"],
        ascending=[False, False]
    ).head(25)
    
    return summary


def _format_user_option(option: str | None, label_map: dict[str, str]) -> str:
    """
    Format selectbox labels for recent activity users.
    """
    if option is None:
        return "최근 활동 사용자에서 선택"
    return label_map.get(option, option)


def _decorate_category(column: pd.Series) -> pd.Series:
    """
    Map raw category codes to localized labels for table output.
    """
    return column.map(CATEGORY_NAME_MAP).fillna(column)


def show():
    """
    Render the user monthly report page.
    """
    st.title("사용자 월간 리포트")
    st.markdown(
        "최근 한달 간 한 사용자가 어떤 이슈를 시청하고 평가했는지, "
        "또 정치 성향 점수가 어떻게 변화했는지를 한눈에 살펴볼 수 있습니다."
    )
    
    with st.spinner("데이터를 로드하는 중입니다..."):
        watch_df = load_user_watch_history()
        evaluation_df = load_issue_evaluations()
        comment_likes_df = load_user_comment_likes()
        score_history_df = load_political_score_history()
        issues_df = load_issues()
        comments_df = load_issue_comments()
        media_df = load_media_sources()
    
    if watch_df.empty:
        st.warning("시청 기록 데이터가 없습니다. 데이터 파일을 확인해주세요.")
        return
    
    # Ensure datetime fields are properly typed
    watch_df = watch_df.copy()
    if "watchedAt" in watch_df.columns:
        watch_df["watchedAt"] = pd.to_datetime(
            watch_df["watchedAt"],
            errors="coerce"
        )
        watch_df = watch_df.dropna(subset=["watchedAt"])
    
    reference_date = datetime.now(timezone.utc)
    
    recent_activity = _prepare_recent_activity_summary(watch_df, reference_date)
    label_map = {}
    if not recent_activity.empty:
        label_map = {
            row["userId"]: (
                f"{row['userId']} · 최근 본 이슈 {row['issue_variety']}개 · "
                f"최근 {row['last_watch'].strftime('%Y-%m-%d')}"
            )
            for _, row in recent_activity.iterrows()
            if pd.notna(row["last_watch"])
        }
    
    if "report_selected_user_id" not in st.session_state:
        st.session_state.report_selected_user_id = None
    
    st.markdown("### 사용자 선택")
    manual_col, select_col = st.columns(2)
    
    with manual_col:
        manual_user_id = st.text_input(
            "사용자 ID 직접 입력",
            value=st.session_state.report_selected_user_id or "",
            placeholder="예: a1B2c3D4...",
        ).strip()
    
    with select_col:
        recent_options = [None] + recent_activity["userId"].tolist() if not recent_activity.empty else [None]
        selected_recent_user = st.selectbox(
            "최근 활동 사용자",
            options=recent_options,
            format_func=lambda option: _format_user_option(option, label_map)
        )
    
    previous_user = st.session_state.report_selected_user_id
    
    if manual_user_id:
        st.session_state.report_selected_user_id = manual_user_id
    elif selected_recent_user:
        st.session_state.report_selected_user_id = selected_recent_user
    elif manual_user_id == "" and selected_recent_user is None:
        # No selection made
        st.session_state.report_selected_user_id = previous_user
    
    user_id = st.session_state.report_selected_user_id
    
    if not user_id:
        st.info("사용자를 선택하거나 ID를 입력하면 상세 리포트를 볼 수 있습니다.")
        
        if not recent_activity.empty:
            st.markdown("#### 최근 한달간 많이 본 사용자 Top 25")
            preview_df = recent_activity.copy()
            preview_df["recent_watch"] = preview_df["last_watch"].dt.strftime("%Y-%m-%d %H:%M")
            preview_df = preview_df.rename(columns={
                "userId": "사용자 ID",
                "issue_variety": "최근 본 이슈 수",
                "recent_watch": "최근 시청"
            })[["사용자 ID", "최근 본 이슈 수", "최근 시청"]]
            st.dataframe(preview_df, use_container_width=True, hide_index=True)
        return
    
    st.markdown(f"### 사용자 {user_id} 리포트")
    
    user_watch_recent = get_user_recent_watch_history(
        watch_df,
        user_id=user_id,
        days=RECENT_WINDOW_DAYS,
        reference_date=reference_date
    )
    
    if user_watch_recent.empty:
        st.warning("최근 한달간 시청 기록이 없습니다. 다른 사용자를 선택해보세요.")
        return
    
    issue_counts = count_user_watch_by_issue(user_watch_recent, issues_df)
    category_counts = count_watch_by_category(issue_counts)
    daily_counts = count_watch_by_day(user_watch_recent)
    
    user_evaluations = filter_user_issue_evaluations(
        evaluation_df,
        user_id=user_id,
        days=RECENT_WINDOW_DAYS,
        reference_date=reference_date
    )
    evaluation_counts = count_evaluations_by_perspective(user_evaluations)
    
    user_comment_likes = filter_user_comment_likes(
        comment_likes_df,
        user_id=user_id,
        days=RECENT_WINDOW_DAYS,
        reference_date=reference_date
    )
    comment_like_counts = count_comment_likes_by_perspective(user_comment_likes)
    comment_like_details = build_comment_like_details(
        user_comment_likes,
        comments_df=comments_df,
        issues_df=issues_df
    )
    
    user_score_recent = filter_user_political_scores(
        score_history_df,
        user_id=user_id,
        days=RECENT_WINDOW_DAYS,
        reference_date=reference_date
    )
    
    media_perspective = summarize_media_perspectives(
        issue_counts=issue_counts,
        issues_df=issues_df,
        media_df=media_df
    )
    
    unique_issues = int(user_watch_recent["issueId"].nunique())
    last_watch = user_watch_recent["watchedAt"].max()
    evaluation_total = int(user_evaluations.shape[0])
    evaluated_issue_count = int(user_evaluations["issueId"].nunique())
    comment_like_total = int(user_comment_likes.shape[0])
    
    top_like_metric_value = "정보 없음"
    if not comment_like_counts.empty:
        top_like = comment_like_counts.sort_values("like_count", ascending=False).iloc[0]
        top_like_label = PERSPECTIVE_LABELS.get(top_like["perspective"], top_like["perspective"])
        top_like_metric_value = f"{top_like_label} · {top_like['like_count']:,}개"
    
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    metrics_col1.metric("최근 본 이슈 수", f"{unique_issues:,}")
    metrics_col2.metric("평가한 이슈 수", f"{evaluated_issue_count:,}")
    metrics_col3.metric("제출한 평가 수", f"{evaluation_total:,}")
    metrics_col4.metric(
        "최근 시청 시점",
        last_watch.strftime("%Y-%m-%d %H:%M") if pd.notna(last_watch) else "정보 없음"
    )
    
    like_metrics_col1, like_metrics_col2 = st.columns(2)
    like_metrics_col1.metric("좋아요한 댓글 수", f"{comment_like_total:,}")
    like_metrics_col2.metric("가장 많이 좋아요한 성향", top_like_metric_value)
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("카테고리별 본 이슈 분포")
        if category_counts.empty:
            st.info("카테고리 정보를 찾을 수 없습니다.")
        else:
            category_fig = create_user_watch_category_bar_chart(category_counts)
            st.plotly_chart(category_fig, use_container_width=True)
    
    with chart_col2:
        st.subheader("이슈 평가 성향")
        evaluation_fig = create_user_evaluation_distribution_chart(evaluation_counts)
        st.plotly_chart(evaluation_fig, use_container_width=True)
    
    st.subheader("좋아요한 댓글 성향")
    liked_comment_fig = create_user_comment_like_distribution_chart(comment_like_counts)
    st.plotly_chart(liked_comment_fig, use_container_width=True)
    
    st.subheader("일자별 본 이슈 수")
    daily_watch_fig = create_user_watch_daily_chart(daily_counts)
    st.plotly_chart(daily_watch_fig, use_container_width=True)
    
    st.subheader("정치 성향 점수 변화")
    if user_score_recent.empty:
        st.info("최근 한달간 업데이트된 정치 성향 점수가 없습니다.")
    else:
        score_fig = create_user_political_journey_chart(user_score_recent, user_id)
        st.plotly_chart(score_fig, use_container_width=True)
    
    st.subheader("시청한 이슈의 언론사 성향 노출")
    media_fig = create_media_perspective_distribution_chart(media_perspective)
    st.plotly_chart(media_fig, use_container_width=True)
    
    st.markdown("#### 좋아요한 댓글 목록")
    if comment_like_details.empty:
        st.info("최근 한달간 좋아요한 댓글이 없습니다.")
    else:
        like_detail = comment_like_details.copy()
        
        if "likedAt" in like_detail.columns:
            liked_at_series = like_detail["likedAt"]
            if pd.api.types.is_datetime64tz_dtype(liked_at_series):
                like_detail["likedAt"] = liked_at_series.dt.tz_convert("Asia/Seoul")
            like_detail["likedAt"] = like_detail["likedAt"].dt.strftime("%Y-%m-%d %H:%M")
        
        if "category" not in like_detail.columns:
            like_detail["category"] = "unknown"
        like_detail["category_label"] = _decorate_category(like_detail["category"])
        
        if "perspective" not in like_detail.columns:
            like_detail["perspective"] = "unknown"
        perspective_base = like_detail["perspective"].fillna("unknown")
        like_detail["perspective_label"] = (
            perspective_base.map(PERSPECTIVE_LABELS).fillna(perspective_base).replace("unknown", "미분류")
        )
        
        if "comment_perspective" not in like_detail.columns:
            like_detail["comment_perspective"] = "unknown"
        comment_perspective_base = like_detail["comment_perspective"].fillna("unknown")
        like_detail["comment_perspective_label"] = (
            comment_perspective_base.map(PERSPECTIVE_LABELS).fillna(comment_perspective_base).replace("unknown", "미분류")
        )
        
        if "comment_content" in like_detail.columns:
            like_detail["comment_content"] = like_detail["comment_content"].fillna("내용을 불러올 수 없습니다.")
            like_detail["comment_content"] = like_detail["comment_content"].str.replace("\n", " ", regex=False)
        
        display_mappings = [
            ("commentId", "댓글 ID"),
            ("issue_title", "이슈 제목"),
            ("category_label", "카테고리"),
            ("perspective_label", "좋아요 시점 성향"),
            ("comment_perspective_label", "현재 댓글 성향"),
            ("likedAt", "좋아요 시점"),
            ("comment_content", "댓글 내용")
        ]
        available_columns = [col for col, _ in display_mappings if col in like_detail.columns]
        rename_map = {col: label for col, label in display_mappings if col in like_detail.columns}
        display_df = like_detail[available_columns].rename(columns=rename_map)
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    st.markdown("#### 남긴 평가 목록")
    if user_evaluations.empty:
        st.info("최근 한달간 남긴 평가가 없습니다.")
    else:
        evaluation_detail = user_evaluations.merge(
            issues_df[["_id", "title", "category"]],
            left_on="issueId",
            right_on="_id",
            how="left"
        )
        evaluation_detail["category_label"] = _decorate_category(evaluation_detail["category"])
        evaluation_detail["evaluatedAt"] = evaluation_detail["evaluatedAt"].dt.strftime("%Y-%m-%d %H:%M")
        evaluation_detail = evaluation_detail.rename(columns={
            "issueId": "이슈 ID",
            "title": "이슈 제목",
            "category_label": "카테고리",
            "perspective": "평가 성향",
            "evaluatedAt": "평가 시점"
        })[["이슈 ID", "이슈 제목", "카테고리", "평가 성향", "평가 시점"]]
        st.dataframe(evaluation_detail, use_container_width=True, hide_index=True)


# Alias for backward compatibility with other modules
show_user_monthly_report_page = show


if __name__ == "__main__":
    show()
