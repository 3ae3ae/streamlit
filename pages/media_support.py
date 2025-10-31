"""
Media source support page.
Displays cumulative support graphs for media sources based on user evaluations.
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
    
    This page shows cumulative support graphs for media sources over time,
    with a clickable interface for selecting media sources.
    """
    st.title("언론사 지지도 분석")
    st.markdown("사용자 평가를 기반으로 각 언론사의 누적 지지도를 확인할 수 있습니다.")
    
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
        with st.spinner("언론사 지지도를 계산하는 중..."):
            support_df = calculate_media_support_scores(
                evaluations_df,
                issues_df,
                media_df
            )
        
        if support_df.empty:
            st.warning("언론사 지지도 데이터를 계산할 수 없습니다. 평가 데이터를 확인해주세요.")
            return
        
        # Get unique media sources with support data
        media_with_support = support_df[["media_id", "media_name"]].drop_duplicates()
        
        if media_with_support.empty:
            st.warning("지지도 데이터가 있는 언론사가 없습니다.")
            return
        
        st.info(f"📊 총 {len(media_with_support)}개 언론사의 지지도 데이터가 있습니다.")
        
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
            help="단일 언론사: 성향별 지지도 표시 | 다중 언론사: 여러 언론사 비교",
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
                
                # Calculate total support for this media
                media_support = support_df[support_df["media_id"] == media_id]
                total_support = 0
                if not media_support.empty:
                    total_support = media_support["cumulative_support"].max()
                    if pd.isna(total_support):
                        total_support = 0
                
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
                    st.caption(f"지지도: {total_support:,}")
                
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
                    st.warning("선택한 언론사에 대한 지지도 데이터가 없습니다.")
                    return
                
                # Display aggregate statistics
                st.markdown("#### 전체 통계")
                col1, col2, col3 = st.columns(3)
                
                # Calculate total support across all selected media
                total_support = 0
                for media_id in selected_media_ids:
                    media_subset = support_df[support_df["media_id"] == media_id]
                    if not media_subset.empty:
                        max_support = media_subset["cumulative_support"].max()
                        total_support += max_support if pd.notna(max_support) else 0
                
                col1.metric("선택된 언론사 수", len(selected_media_ids))
                col2.metric("총 누적 지지도", f"{total_support:,}")
                col3.metric("평균 지지도", f"{total_support // len(selected_media_ids):,}" if len(selected_media_ids) > 0 else "0")
                
                # Create and display comparison chart
                with st.spinner("비교 차트를 생성하는 중..."):
                    fig = create_media_support_chart(support_df, media_ids=selected_media_ids)
                
                st.plotly_chart(fig, width="stretch")
                
                # Display individual media statistics
                with st.expander("개별 언론사 통계"):
                    for media_id in selected_media_ids:
                        media_subset = support_df[support_df["media_id"] == media_id]
                        if not media_subset.empty:
                            media_name = media_subset["media_name"].iloc[0]
                            max_support = media_subset["cumulative_support"].max()
                            
                            st.markdown(f"**{media_name}**")
                            st.write(f"총 누적 지지도: {max_support:,}")
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
                    st.warning(f"언론사 '{media_name}'에 대한 지지도 데이터가 없습니다.")
                    return
                
                # Display statistics
                col1, col2, col3 = st.columns(3)
                
                # Calculate total support by perspective
                left_support = media_data[media_data["perspective"] == "left"]["cumulative_support"].max() if not media_data[media_data["perspective"] == "left"].empty else 0
                center_support = media_data[media_data["perspective"] == "center"]["cumulative_support"].max() if not media_data[media_data["perspective"] == "center"].empty else 0
                right_support = media_data[media_data["perspective"] == "right"]["cumulative_support"].max() if not media_data[media_data["perspective"] == "right"].empty else 0
                
                col1.metric("진보 지지도", f"{left_support:,}")
                col2.metric("중도 지지도", f"{center_support:,}")
                col3.metric("보수 지지도", f"{right_support:,}")
                
                # Create and display chart
                with st.spinner("차트를 생성하는 중..."):
                    fig = create_media_support_chart(support_df, media_id=selected_media_id)
                
                st.plotly_chart(fig, width="stretch")
            
            # Display additional information
            with st.expander("지지도 계산 방법"):
                st.markdown("""
                ### 지지도 계산 로직
                언론사의 지지도는 다음과 같이 계산됩니다:
                
                1. **사용자 평가**: 사용자가 특정 이슈에 대해 진보/중도/보수 중 하나의 성향에 동의
                2. **언론사 매칭**: 해당 이슈를 보도한 언론사 중 동일한 성향의 언론사를 찾음
                3. **지지도 증가**: 매칭된 언론사의 해당 성향 지지도에 +1
                4. **누적 계산**: 시간에 따라 지지도를 누적하여 표시
                
                ### 성향별 지지도
                - **진보 지지도**: 진보 성향 이슈에 대한 사용자 동의 기반
                - **중도 지지도**: 중도 성향 이슈에 대한 사용자 동의 기반
                - **보수 지지도**: 보수 성향 이슈에 대한 사용자 동의 기반
                
                ### 차트 해석
                - 그래프가 가파르게 상승하면 해당 기간에 많은 지지를 받았음을 의미
                - 평평한 구간은 지지도 변화가 없는 기간
                - 성향별로 다른 색상으로 표시되어 비교가 용이
                """)
            
            # Display recent support events
            with st.expander("최근 지지도 변화"):
                recent_data = media_data.sort_values("date", ascending=False).head(10)
                
                st.markdown("### 최근 10개 기록")
                
                for _, row in recent_data.iterrows():
                    date = row["date"].strftime("%Y-%m-%d")
                    perspective = row["perspective"]
                    support_count = row["support_count"]
                    cumulative = row["cumulative_support"]
                    
                    perspective_label = {
                        "left": "진보",
                        "center": "중도",
                        "right": "보수"
                    }.get(perspective, perspective)
                    
                    st.write(f"**{date}** - {perspective_label}: +{support_count} (누적: {cumulative:,})")
        else:
            st.info("👆 위의 목록에서 언론사를 클릭하여 선택하세요.")
            
            if view_mode == "다중 언론사 비교":
                st.markdown("""
                **다중 언론사 비교 모드**
                - 여러 언론사를 클릭하여 선택할 수 있습니다 (최대 7개)
                - 선택된 언론사를 다시 클릭하면 선택이 해제됩니다
                - 선택된 언론사들의 지지도를 한 차트에서 비교할 수 있습니다
                """)
            else:
                st.markdown("""
                **단일 언론사 모드**
                - 하나의 언론사를 클릭하여 선택할 수 있습니다
                - 선택된 언론사의 성향별 지지도를 확인할 수 있습니다
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
