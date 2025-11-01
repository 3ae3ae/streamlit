"""
Media source support page.
Displays rolling support ratio charts for media sources based on user evaluations.
"""

import logging
import pandas as pd
import streamlit as st

from data_loader import load_issue_evaluations, load_issues, load_media_sources
from processing.aggregators import calculate_media_support_scores
from visualizations.charts import create_media_support_chart


def show():
    """
    Display the media source support page.
    
    This page shows rolling support ratio graphs for media sources,
    with a clickable interface for selecting media sources.
    """
    st.title("언론사 지지도 분석")
    st.markdown("사용자 평가를 기반으로 최근 3일간의 언론사 지지율 변화를 확인할 수 있습니다.")
    
    try:
        # Load data
        with st.spinner("데이터를 로드하는 중..."):
            evaluations_df = load_issue_evaluations()
            issues_df = load_issues()
            media_df = load_media_sources()
        
        if evaluations_df.empty:
            st.warning("이슈 평가 데이터가 없습니다.")
            return
        
        if issues_df.empty:
            st.warning("이슈 데이터가 없습니다.")
            return
        
        if media_df.empty:
            st.warning("언론사 데이터가 없습니다.")
            return
        
        # Calculate media support scores
        with st.spinner("언론사 지지율을 계산하는 중..."):
            support_df = calculate_media_support_scores(
                evaluations_df,
                issues_df,
                media_df
            )
        
        if support_df.empty:
            st.warning("언론사 지지율 데이터를 계산할 수 없습니다. 평가 데이터를 확인해주세요.")
            return
        
        # Get unique media sources with support data
        media_with_support = support_df[["media_id", "media_name"]].drop_duplicates()
        
        if media_with_support.empty:
            st.warning("지지율 데이터가 있는 언론사가 없습니다.")
            return
        
        st.info(f"📊 총 {len(media_with_support)}개 언론사의 지지율 데이터가 있습니다.")
        
        # Initialize session state for selected media
        if "selected_media_ids" not in st.session_state:
            st.session_state.selected_media_ids = []
        if "media_view_mode" not in st.session_state:
            st.session_state.media_view_mode = "단일 언론사"
        
        # Media selection UI
        st.markdown("### 언론사 선택")
        
        # View mode selection
        view_mode = st.radio(
            "보기 모드",
            options=["단일 언론사", "다중 언론사 비교"],
            horizontal=True,
            help="단일 언론사: 성향별 지지율 표시 | 다중 언론사: 여러 언론사 지지율 비교",
            index=0 if st.session_state.media_view_mode == "단일 언론사" else 1
        )
        
        # Update session state if view mode changed
        if view_mode != st.session_state.media_view_mode:
            st.session_state.media_view_mode = view_mode
            # Clear selection when switching modes
            st.session_state.selected_media_ids = []
        
        # Create media options dictionary
        media_options = {}
        for _, row in media_with_support.iterrows():
            media_id = row["media_id"]
            media_name = row["media_name"]
            media_options[f"{media_name} ({media_id})"] = media_id
        
        # Clickable media list
        st.markdown("### 클릭하여 선택")
        st.info("아래 목록에서 언론사를 클릭하여 선택할 수 있습니다.")
        
        # Sort by name
        sorted_media = media_with_support.sort_values("media_name")
        
        # Display clickable list
        with st.container():
            for idx, (_, row) in enumerate(sorted_media.iterrows(), 1):
                media_id = row["media_id"]
                media_name = row["media_name"]
                
                # Calculate recent support ratio for this media
                media_support = support_df[support_df["media_id"] == media_id]
                recent_ratio = None
                if not media_support.empty:
                    media_support = media_support.sort_values("date")
                    latest_date = media_support["date"].max()
                    latest_rows = media_support[media_support["date"] == latest_date]
                    numerator = latest_rows["window_supported_issue_count"].sum()
                    denominator = latest_rows["window_issue_count"].sum()
                    if denominator > 0:
                        recent_ratio = (numerator / denominator) * 100
                
                if recent_ratio is not None and pd.notna(recent_ratio):
                    ratio_caption = f"{recent_ratio:.1f}%"
                else:
                    ratio_caption = "데이터 없음"
                
                # Check if this media is currently selected
                is_selected = media_id in st.session_state.selected_media_ids
                
                # Display media with button
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    # Use different button type for selected media
                    button_type = "primary" if is_selected else "secondary"
                    button_label = f"{'✓ ' if is_selected else ''}{idx}. {media_name}"
                    
                    if st.button(
                        button_label,
                        key=f"media_{media_id}",
                        help=f"언론사 ID: {media_id}",
                        type=button_type
                    ):
                        if view_mode == "단일 언론사":
                            # Single mode: replace selection
                            st.session_state.selected_media_ids = [media_id]
                        else:
                            # Multi mode: toggle selection
                            if media_id in st.session_state.selected_media_ids:
                                st.session_state.selected_media_ids.remove(media_id)
                            else:
                                # Check max limit
                                if len(st.session_state.selected_media_ids) < 7:
                                    st.session_state.selected_media_ids.append(media_id)
                                else:
                                    st.warning("최대 7개 언론사까지 선택할 수 있습니다.")
                        st.rerun()
                
                with col2:
                    st.caption(f"최근 3일 지지율: {ratio_caption}")
                
                # Add separator
                if idx < len(sorted_media):
                    st.divider()
        
        # Use selected media from session state
        selected_media_ids = st.session_state.selected_media_ids
        is_multi_mode = (view_mode == "다중 언론사 비교")
        
        # Display selected media chart
        if selected_media_ids and len(selected_media_ids) > 0:
            if is_multi_mode:
                st.markdown(f"### 선택된 언론사 ({len(selected_media_ids)}개)")
                
                # Display selected media list
                for media_id in selected_media_ids:
                    media_info = media_with_support[media_with_support["media_id"] == media_id]
                    if not media_info.empty:
                        media_name = media_info.iloc[0]["media_name"]
                        st.write(f"• {media_name} ({media_id})")
                
                # Get data for all selected media
                media_data = support_df[support_df["media_id"].isin(selected_media_ids)]
                
                if media_data.empty:
                    st.warning("선택한 언론사에 대한 지지율 데이터가 없습니다.")
                    return
                
                # Display aggregate statistics
                st.markdown("#### 전체 통계")
                col1, col2, col3 = st.columns(3)
                
                latest_ratios = []
                for media_id in selected_media_ids:
                    media_subset = support_df[support_df["media_id"] == media_id]
                    if media_subset.empty:
                        continue
                    
                    media_subset = media_subset.sort_values("date")
                    latest_date = media_subset["date"].max()
                    latest_rows = media_subset[media_subset["date"] == latest_date]
                    numerator = latest_rows["window_supported_issue_count"].sum()
                    denominator = latest_rows["window_issue_count"].sum()
                    
                    if denominator > 0:
                        latest_ratios.append((numerator / denominator) * 100)
                
                avg_ratio = sum(latest_ratios) / len(latest_ratios) if latest_ratios else None
                max_ratio = max(latest_ratios) if latest_ratios else None
                
                col1.metric("선택된 언론사 수", len(selected_media_ids))
                col2.metric(
                    "평균 3일 지지율",
                    f"{avg_ratio:.1f}%" if avg_ratio is not None else "데이터 없음"
                )
                col3.metric(
                    "최고 3일 지지율",
                    f"{max_ratio:.1f}%" if max_ratio is not None else "데이터 없음"
                )
                
                # Create and display comparison chart
                with st.spinner("비교 차트를 생성하는 중..."):
                    fig = create_media_support_chart(support_df, media_ids=selected_media_ids)
                
                st.plotly_chart(fig, width="stretch")
                
                # Display individual media statistics
                with st.expander("개별 언론사 통계"):
                    for media_id in selected_media_ids:
                        media_subset = support_df[support_df["media_id"] == media_id]
                        if not media_subset.empty:
                            media_subset = media_subset.sort_values("date")
                            media_name = media_subset["media_name"].iloc[0]
                            latest_date = media_subset["date"].max()
                            latest_rows = media_subset[media_subset["date"] == latest_date]
                            numerator = latest_rows["window_supported_issue_count"].sum()
                            denominator = latest_rows["window_issue_count"].sum()
                            
                            ratio_text = "데이터 없음"
                            issues_text = "-"
                            if denominator > 0:
                                ratio_text = f"{(numerator / denominator) * 100:.1f}%"
                                issues_text = f"{int(denominator):,}"
                            
                            st.markdown(f"**{media_name}**")
                            st.write(f"최근 3일 지지율: {ratio_text}")
                            st.write(f"최근 3일 전체 이슈 수: {issues_text}")
                            st.divider()
                
            else:
                # Single media mode
                selected_media_id = selected_media_ids[0]
                
                # Get media name
                media_info = media_with_support[media_with_support["media_id"] == selected_media_id]
                if not media_info.empty:
                    media_name = media_info.iloc[0]["media_name"]
                    st.markdown(f"### 선택된 언론사: {media_name} ({selected_media_id})")
                else:
                    st.markdown(f"### 선택된 언론사: {selected_media_id}")
                
                # Get media-specific data
                media_data = support_df[support_df["media_id"] == selected_media_id]
                
                if media_data.empty:
                    media_info = media_with_support[media_with_support["media_id"] == selected_media_id]
                    media_name = media_info.iloc[0]["media_name"] if not media_info.empty else selected_media_id
                    st.warning(f"언론사 '{media_name}'에 대한 지지율 데이터를 찾을 수 없습니다.")
                    return
                
                # Display statistics
                col1, col2, col3 = st.columns(3)
                
                perspective_labels = [
                    ("left", "진보 3일 지지율"),
                    ("center", "중도 3일 지지율"),
                    ("right", "보수 3일 지지율")
                ]
                columns = [col1, col2, col3]
                
                for (perspective_key, label), column in zip(perspective_labels, columns):
                    perspective_data = media_data[media_data["perspective"] == perspective_key].sort_values("date")
                    if perspective_data.empty:
                        column.metric(label, "데이터 없음")
                        continue
                    
                    last_row = perspective_data.iloc[-1]
                    ratio_value = last_row.get("support_ratio")
                    
                    if ratio_value is not None and pd.notna(ratio_value):
                        column.metric(label, f"{ratio_value:.1f}%")
                    else:
                        column.metric(label, "데이터 없음")
                
                # Create and display chart
                with st.spinner("차트를 생성하는 중..."):
                    fig = create_media_support_chart(support_df, media_id=selected_media_id)
                
                st.plotly_chart(fig, width="stretch")
            
            # Display additional information
            with st.expander("지지율 계산 방법"):
                st.markdown("""
                ### 지지율 계산 로직
                언론사의 지지율은 다음 단계를 통해 산출됩니다:
                
                1. **사용자 평가**: 사용자가 특정 이슈에서 동의한 정치 성향(진보/중도/보수)을 수집합니다.
                2. **언론사 매칭**: 동일한 성향으로 이슈를 보도한 언론사를 매칭합니다.
                3. **이슈 집계**: 해당 언론사가 최근 3일 동안 다룬 이슈 수와 지지를 받은 이슈 수를 계산합니다.
                4. **비율 계산**: 지지를 받은 이슈 수 ÷ 전체 이슈 수 × 100으로 3일 지지율(%)을 구합니다.
                
                ### 성향별 지지율
                - **진보 지지율**: 진보·중도진보 성향 보도를 지지한 이슈 비율
                - **중도 지지율**: 중도 성향 보도를 지지한 이슈 비율
                - **보수 지지율**: 중도보수·보수 성향 보도를 지지한 이슈 비율
                
                ### 차트 해석
                - 그래프 상승: 최근 3일 동안 지지 비율이 높아졌음을 의미합니다.
                - 그래프 하락: 최근 사용자 지지가 감소했음을 의미합니다.
                - 평평한 구간: 최근 3일간 지지율 변화가 없음을 의미합니다.
                """)
            
            # Display recent support events
            with st.expander("최근 지지율 변화"):
                recent_data = media_data.sort_values("date", ascending=False).head(10)
                
                st.markdown("### 최근 10개 기록")
                
                for _, row in recent_data.iterrows():
                    date = row["date"].strftime("%Y-%m-%d")
                    perspective = row["perspective"]
                    ratio_value = row.get("support_ratio")
                    window_supported = row.get("window_supported_issue_count")
                    window_total = row.get("window_issue_count")
                    daily_supported = row.get("daily_supported_issue_count")
                    daily_total = row.get("daily_issue_count")
                    
                    perspective_label = {
                        "left": "진보",
                        "center": "중도",
                        "right": "보수"
                    }.get(perspective, perspective)
                    
                    ratio_text = f"{ratio_value:.1f}%" if ratio_value is not None and pd.notna(ratio_value) else "데이터 없음"
                    window_text = "-"
                    if window_total is not None and pd.notna(window_total) and window_total > 0:
                        supported_val = int(window_supported) if window_supported is not None and pd.notna(window_supported) else 0
                        total_val = int(window_total)
                        window_text = f"{supported_val:,}/{total_val:,}"
                    
                    daily_text = "-"
                    if daily_total is not None and pd.notna(daily_total) and daily_total > 0:
                        daily_supported_val = int(daily_supported) if daily_supported is not None and pd.notna(daily_supported) else 0
                        daily_total_val = int(daily_total)
                        daily_text = f"{daily_supported_val:,}/{daily_total_val:,}"
                    
                    st.write(
                        f"**{date}** - {perspective_label}: {ratio_text} "
                        f"(3일 지지 이슈 {window_text}, 일일 지지 {daily_text})"
                    )
        else:
            st.info("👆 위의 목록에서 언론사를 클릭하여 선택하세요.")
            
            if view_mode == "다중 언론사 비교":
                st.markdown("""
                **다중 언론사 비교 모드**
                - 여러 언론사를 클릭하여 선택할 수 있습니다 (최대 7개)
                - 선택된 언론사를 다시 클릭하면 선택이 해제됩니다
                - 선택된 언론사들의 지지율을 한 차트에서 비교할 수 있습니다
                """)
            else:
                st.markdown("""
                **단일 언론사 모드**
                - 하나의 언론사를 클릭하여 선택할 수 있습니다
                - 선택된 언론사의 성향별 지지율을 확인할 수 있습니다
                """)
        
    except FileNotFoundError as e:
        st.error("📁 데이터 파일을 찾을 수 없습니다")
        st.info("data 폴더에 필요한 JSON 파일들(prod.userIssueEvaluations.json, prod.issues.json, prod.mediaSources.json)이 있는지 확인해주세요.")
        logging.error(f"File not found in media support page: {e}")
    except PermissionError as e:
        st.error("🔒 데이터 파일에 접근할 수 없습니다")
        st.info("파일 권한을 확인해주세요.")
        logging.error(f"Permission error in media support page: {e}")
    except Exception as e:
        st.error("❌ 예상치 못한 오류가 발생했습니다")
        st.info("페이지를 새로고침하거나 다른 페이지를 시도해보세요.")
        logging.error(f"Error in media support page: {e}", exc_info=True)
        
        # Show detailed error in expander for debugging
        with st.expander("🔍 상세 오류 정보 (개발자용)"):
            st.code(str(e))


# Alias for backward compatibility
show_media_support_page = show


if __name__ == "__main__":
    show()
