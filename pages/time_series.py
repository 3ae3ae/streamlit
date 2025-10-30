"""
Time series political preference change page.
Displays time-series graphs showing how political scores change over time.
"""

from datetime import datetime, timedelta
import logging

import streamlit as st

from data_loader import load_political_score_history
from processing.aggregators import aggregate_political_scores_by_date
from visualizations.charts import create_time_series_chart


def show():
    """
    Display the time series political preference change page.
    
    This page shows time-series graphs with filters for date range (7/30 days),
    view type (category/average), and category selection.
    """
    st.title("시간별 정치 성향 변화")
    st.markdown("시간에 따른 정치 성향 점수의 변화를 추적할 수 있습니다.")
    
    try:
        # Load political score history
        with st.spinner("정치 성향 히스토리 데이터를 로드하는 중..."):
            history_df = load_political_score_history()
        
        if history_df.empty:
            st.warning("정치 성향 히스토리 데이터가 없습니다.")
            return
        
        # Sidebar filters
        st.sidebar.header("필터 설정")
        
        # Date range filter
        date_range_option = st.sidebar.radio(
            "날짜 범위",
            options=["7일", "30일"],
            index=0
        )
        
        # Calculate date range
        end_date = datetime.now()
        if date_range_option == "7일":
            start_date = end_date - timedelta(days=7)
            date_range = "7d"
        else:
            start_date = end_date - timedelta(days=30)
            date_range = "30d"
        
        # View type toggle
        view_type_option = st.sidebar.radio(
            "보기 유형",
            options=["카테고리별", "전체 평균"],
            index=0
        )
        
        view_type = "category" if view_type_option == "카테고리별" else "average"
        
        # Category selection (only shown for category view)
        category = None
        if view_type == "category":
            category_map = {
                "정치": "politics",
                "경제": "economy",
                "사회": "society",
                "문화": "culture",
                "기술": "technology",
                "국제": "international"
            }
            
            category_label = st.sidebar.selectbox(
                "카테고리 선택",
                options=list(category_map.keys()),
                index=0
            )
            
            category = category_map[category_label]
        
        # Aggregate data
        with st.spinner("데이터를 집계하는 중..."):
            aggregated_df = aggregate_political_scores_by_date(
                history_df,
                start_date,
                end_date
            )
        
        if aggregated_df.empty:
            st.warning(f"선택한 기간({date_range_option})에 데이터가 없습니다.")
            return
        
        # Display date range info
        st.info(f"📅 표시 기간: {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")
        
        # Create and display time series chart
        fig = create_time_series_chart(
            aggregated_df,
            date_range,
            view_type,
            category
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Display additional information
        with st.expander("차트 사용 방법"):
            st.markdown("""
            ### 인터랙티브 기능
            - **줌**: 차트를 드래그하여 특정 영역을 확대할 수 있습니다
            - **팬**: 확대 후 차트를 이동할 수 있습니다
            - **호버**: 데이터 포인트에 마우스를 올리면 상세 정보를 볼 수 있습니다
            - **범례**: 범례 항목을 클릭하여 특정 성향을 숨기거나 표시할 수 있습니다
            - **리셋**: 더블 클릭하여 원래 뷰로 돌아갈 수 있습니다
            
            ### 성향 설명
            - **진보**: 진보적 성향 점수 비율
            - **중도**: 중도 성향 점수 비율
            - **보수**: 보수적 성향 점수 비율
            """)
        
        # Display statistics
        with st.expander("통계 정보"):
            if view_type == "category" and category:
                category_data = aggregated_df[aggregated_df["category"] == category]
                if not category_data.empty:
                    avg_left = category_data["left_proportion"].mean() * 100
                    avg_center = category_data["center_proportion"].mean() * 100
                    avg_right = category_data["right_proportion"].mean() * 100
                    
                    st.markdown(f"### {category_label} 카테고리 평균")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("진보", f"{avg_left:.1f}%")
                    col2.metric("중도", f"{avg_center:.1f}%")
                    col3.metric("보수", f"{avg_right:.1f}%")
            else:
                # Calculate overall average
                avg_left = aggregated_df["left_proportion"].mean() * 100
                avg_center = aggregated_df["center_proportion"].mean() * 100
                avg_right = aggregated_df["right_proportion"].mean() * 100
                
                st.markdown("### 전체 평균")
                col1, col2, col3 = st.columns(3)
                col1.metric("진보", f"{avg_left:.1f}%")
                col2.metric("중도", f"{avg_center:.1f}%")
                col3.metric("보수", f"{avg_right:.1f}%")
    
    except FileNotFoundError as e:
        st.error("📁 데이터 파일을 찾을 수 없습니다")
        st.info("data 폴더에 prod.userPoliticalScoreHistory.json 파일이 있는지 확인해주세요.")
        logging.error(f"File not found in time series page: {e}")
    except PermissionError as e:
        st.error("🔒 데이터 파일에 접근할 수 없습니다")
        st.info("파일 권한을 확인해주세요.")
        logging.error(f"Permission error in time series page: {e}")
    except ValueError as e:
        st.error("⚠️ 데이터 형식 오류가 발생했습니다")
        st.info("데이터 파일의 형식이 올바른지 확인해주세요.")
        logging.error(f"Value error in time series page: {e}")
    except Exception as e:
        st.error("❌ 예상치 못한 오류가 발생했습니다")
        st.info("페이지를 새로고침하거나 다른 페이지를 시도해보세요.")
        logging.error(f"Error in time series page: {e}", exc_info=True)
        
        # Show detailed error in expander for debugging
        with st.expander("🔍 상세 오류 정보 (개발자용)"):
            st.code(str(e))


# Alias for backward compatibility
show_time_series_page = show
