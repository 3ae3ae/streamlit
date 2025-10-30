"""
MongoDB Data Visualization Tool - Main Application

This is the main entry point for the Streamlit application that visualizes
MongoDB data including political preferences, topics, issues, and media sources.
"""

import logging
import streamlit as st

# Import all page modules
from pages import (
    issue_evaluation,
    media_support,
    overall_preference,
    time_series,
    topic_wordcloud,
    user_journey
)


def main():
    """
    Main application entry point.
    
    Configures Streamlit page settings, creates sidebar navigation,
    and routes to the appropriate page based on user selection.
    """
    try:
        # Page configuration
        st.set_page_config(
            page_title="MongoDB 데이터 시각화",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                "About": "MongoDB 데이터 시각화 도구 - 정치 성향, 토픽, 이슈, 언론사 분석"
            }
        )
    except Exception:
        # Page config can only be set once, ignore if already set
        pass
    
    # Application header
    st.sidebar.title("📊 MongoDB 데이터 시각화")
    st.sidebar.markdown("---")
    
    # Navigation menu
    st.sidebar.header("시각화 선택")
    
    # Define page functions dictionary for routing
    page_functions = {
        "전체 성향 분포": overall_preference.show,
        "시간별 성향 변화": time_series.show,
        "인기 토픽 워드클라우드": topic_wordcloud.show,
        "개인 성향 변화": user_journey.show,
        "언론사 지지도": media_support.show,
        "이슈 평가 분포": issue_evaluation.show
    }
    
    page = st.sidebar.selectbox(
        "페이지를 선택하세요",
        options=list(page_functions.keys()),
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Display information about the selected page
    page_descriptions = {
        "전체 성향 분포": "모든 사용자의 정치 성향 분포를 원 그래프로 표시합니다.",
        "시간별 성향 변화": "시간에 따른 정치 성향 점수 변화를 추적합니다.",
        "인기 토픽 워드클라우드": "구독자 수가 많은 인기 토픽을 워드클라우드로 시각화합니다.",
        "개인 성향 변화": "특정 사용자의 정치 성향 변화를 시간에 따라 추적합니다.",
        "언론사 지지도": "사용자 평가를 기반으로 언론사의 누적 지지도를 분석합니다.",
        "이슈 평가 분포": "특정 이슈에 대한 사용자 평가 분포를 확인합니다."
    }
    
    st.sidebar.info(page_descriptions[page])
    
    # Add footer
    st.sidebar.markdown("---")
    st.sidebar.caption("💡 각 페이지에서 인터랙티브하게 데이터를 탐색할 수 있습니다.")
    
    # Route to the selected page with error handling
    try:
        page_function = page_functions.get(page)
        if page_function:
            page_function()
        else:
            st.error(f"❌ 페이지 '{page}'를 찾을 수 없습니다")
            logging.error(f"Page function not found for: {page}")
    except Exception as e:
        st.error("❌ 페이지를 로드하는 중 오류가 발생했습니다")
        st.info("페이지를 새로고침하거나 다른 페이지를 선택해보세요.")
        
        logging.error(f"Error loading page {page}: {e}", exc_info=True)
        
        with st.expander("🔍 상세 오류 정보 (개발자용)"):
            st.code(str(e))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error("❌ 애플리케이션을 시작하는 중 오류가 발생했습니다")
        st.info("애플리케이션을 다시 시작해주세요.")
        
        import logging
        logging.error(f"Fatal error in main: {e}", exc_info=True)
