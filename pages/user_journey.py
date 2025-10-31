"""
Individual user political journey page.
Displays a time-series graph showing how a specific user's political scores change over time.
"""

import logging
import streamlit as st

from data_loader import load_political_score_history
from visualizations.charts import create_user_political_journey_chart


def show():
    """
    Display the individual user political journey page.
    
    This page shows a time-series graph of a specific user's political score history
    across all six categories, with error handling for non-existent user IDs.
    """
    st.title("개인 성향 변화 추적")
    st.markdown("특정 사용자의 정치 성향 변화를 시간에 따라 추적할 수 있습니다.")
    
    try:
        # Load political score history
        with st.spinner("정치 성향 히스토리 데이터를 로드하는 중..."):
            history_df = load_political_score_history()
        
        if history_df.empty:
            st.warning("정치 성향 히스토리 데이터가 없습니다.")
            return
        
        # Initialize session state for selected user
        if "selected_user_id" not in st.session_state:
            st.session_state.selected_user_id = None
        
        # User ID input
        st.markdown("### 사용자 ID 입력")
        manual_user_id = st.text_input(
            "사용자 ID",
            value=st.session_state.selected_user_id if st.session_state.selected_user_id else "",
            placeholder="사용자 ID를 입력하세요",
            help="추적하고 싶은 사용자의 ID를 입력하세요"
        )
        
        # Update session state if manual input is provided
        if manual_user_id and manual_user_id != st.session_state.selected_user_id:
            st.session_state.selected_user_id = manual_user_id
        
        # Get recent active users (users with most recent activity)
        st.markdown("### 최근 활동 사용자")
        st.info("아래 목록에서 사용자를 클릭하여 선택할 수 있습니다.")
        
        if "userId" in history_df.columns and "createdAt" in history_df.columns:
            # Get users with their most recent activity
            user_activity = history_df.groupby("userId").agg({
                "createdAt": "max",
                "userId": "count"
            }).rename(columns={"userId": "record_count"})
            user_activity = user_activity.sort_values("createdAt", ascending=False).head(20)
            
            # Display clickable user list
            with st.container():
                for idx, (uid, row) in enumerate(user_activity.iterrows(), 1):
                    last_activity = row["createdAt"]
                    record_count = row["record_count"]
                    
                    # Check if this user is currently selected
                    is_selected = (st.session_state.selected_user_id == uid)
                    
                    # Display user with button
                    col1, col2, col3 = st.columns([3, 2, 1])
                    
                    with col1:
                        # Use different button type for selected user
                        button_type = "primary" if is_selected else "secondary"
                        if st.button(
                            f"{'✓ ' if is_selected else ''}{idx}. 사용자 {uid}",
                            key=f"user_{uid}",
                            type=button_type
                        ):
                            st.session_state.selected_user_id = uid
                            st.rerun()
                    
                    with col2:
                        st.caption(f"최근: {last_activity.strftime('%Y-%m-%d')}")
                    
                    with col3:
                        st.caption(f"{record_count}개 기록")
                    
                    # Add separator
                    if idx < len(user_activity):
                        st.divider()
        else:
            st.warning("사용자 활동 정보를 찾을 수 없습니다.")
        
        # Use the selected user ID from session state
        user_id = st.session_state.selected_user_id
        
        # Process and display chart if user ID is provided
        if user_id:
            # Check if user exists
            user_data = history_df[history_df["userId"] == user_id]
            
            if user_data.empty:
                st.error(f"❌ 사용자 ID '{user_id}'에 대한 데이터를 찾을 수 없습니다.")
                st.info("위의 '사용 가능한 사용자 ID 샘플'을 펼쳐서 유효한 사용자 ID를 확인하세요.")
                return
            
            # Display user statistics
            st.success(f"✅ 사용자 '{user_id}'의 데이터를 찾았습니다.")
            
            col1, col2 = st.columns(2)
            col1.metric("기록 수", f"{len(user_data):,}")
            
            if "createdAt" in user_data.columns and not user_data["createdAt"].isna().all():
                date_range = f"{user_data['createdAt'].min().strftime('%Y-%m-%d')} ~ {user_data['createdAt'].max().strftime('%Y-%m-%d')}"
                col2.metric("기록 기간", date_range)
            
            # Create and display chart
            with st.spinner("차트를 생성하는 중..."):
                fig = create_user_political_journey_chart(history_df, user_id)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display additional information
            with st.expander("차트 해석 방법"):
                st.markdown("""
                ### 차트 설명
                이 차트는 사용자의 6개 카테고리별 정치 성향 점수 변화를 보여줍니다.
                
                ### 점수 계산
                - **양수 값**: 진보 성향이 강함 (진보 점수 - 보수 점수)
                - **0 근처**: 중도 성향
                - **음수 값**: 보수 성향이 강함 (보수 점수 - 진보 점수)
                
                ### 카테고리
                - **정치**: 정치 관련 이슈에 대한 성향
                - **경제**: 경제 정책에 대한 성향
                - **사회**: 사회 이슈에 대한 성향
                - **문화**: 문화 관련 이슈에 대한 성향
                - **기술**: 기술 정책에 대한 성향
                - **국제**: 국제 관계에 대한 성향
                
                ### 인터랙티브 기능
                - **줌**: 차트를 드래그하여 특정 기간을 확대할 수 있습니다
                - **호버**: 데이터 포인트에 마우스를 올리면 정확한 값을 볼 수 있습니다
                - **범례**: 범례 항목을 클릭하여 특정 카테고리를 숨기거나 표시할 수 있습니다
                - **리셋**: 더블 클릭하여 원래 뷰로 돌아갈 수 있습니다
                """)
            
            # Display latest scores
            with st.expander("최근 성향 점수"):
                latest_record = user_data.sort_values("createdAt", ascending=False).iloc[0]
                
                st.markdown("### 최근 기록 시점")
                if "createdAt" in latest_record.index:
                    st.write(f"**날짜**: {latest_record['createdAt'].strftime('%Y-%m-%d %H:%M:%S')}")
                
                st.markdown("### 카테고리별 점수")
                
                categories = {
                    "정치": "politics",
                    "경제": "economy",
                    "사회": "society",
                    "문화": "culture",
                    "기술": "technology",
                    "국제": "international"
                }
                
                for label, cat in categories.items():
                    left_col = f"{cat}_left"
                    center_col = f"{cat}_center"
                    right_col = f"{cat}_right"
                    
                    if all(col in latest_record.index for col in [left_col, center_col, right_col]):
                        left_score = latest_record[left_col]
                        center_score = latest_record[center_col]
                        right_score = latest_record[right_col]
                        
                        st.write(f"**{label}**: 진보 {left_score:.1f} | 중도 {center_score:.1f} | 보수 {right_score:.1f}")
        else:
            st.info("👆 위의 입력 필드에 사용자 ID를 입력하여 해당 사용자의 정치 성향 변화를 확인하세요.")
    
    except FileNotFoundError as e:
        st.error("📁 데이터 파일을 찾을 수 없습니다")
        st.info("data 폴더에 prod.userPoliticalScoreHistory.json 파일이 있는지 확인해주세요.")
        logging.error(f"File not found in user journey page: {e}")
    except PermissionError as e:
        st.error("🔒 데이터 파일에 접근할 수 없습니다")
        st.info("파일 권한을 확인해주세요.")
        logging.error(f"Permission error in user journey page: {e}")
    except Exception as e:
        st.error("❌ 예상치 못한 오류가 발생했습니다")
        st.info("페이지를 새로고침하거나 다른 페이지를 시도해보세요.")
        logging.error(f"Error in user journey page: {e}", exc_info=True)
        
        # Show detailed error in expander for debugging
        with st.expander("🔍 상세 오류 정보 (개발자용)"):
            st.code(str(e))


# Alias for backward compatibility
show_user_journey_page = show


if __name__ == "__main__":
    show()
