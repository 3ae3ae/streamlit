"""
Overall political preference distribution page.
Displays a pie chart showing the distribution of political preferences across all users.
"""

import logging
import streamlit as st

from data_loader import load_users
from visualizations.charts import create_political_preference_pie_chart


def show():
    """
    Display the overall political preference distribution page.
    
    This page shows a pie chart of political preference distribution across all users,
    handling empty values appropriately.
    """
    st.title("전체 사용자 정치 성향 분포")
    st.markdown("모든 사용자의 정치 성향 분포를 확인할 수 있습니다.")
    
    try:
        # Load user data
        with st.spinner("사용자 데이터를 로드하는 중..."):
            users_df = load_users()
        
        if users_df.empty:
            st.warning("사용자 데이터가 없습니다.")
            return
        
        # Display statistics
        total_users = len(users_df)
        st.metric("전체 사용자 수", f"{total_users:,}")
        
        # Create and display pie chart
        fig = create_political_preference_pie_chart(users_df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display additional information
        with st.expander("상세 정보"):
            if "politicalPreference" in users_df.columns:
                preference_counts = users_df["politicalPreference"].fillna("unknown").value_counts()
                
                st.markdown("### 성향별 사용자 수")
                
                label_map = {
                    "left": "진보",
                    "center_left": "중도진보",
                    "center": "중도",
                    "center_right": "중도보수",
                    "right": "보수",
                    "unknown": "미분류"
                }
                
                for pref, count in preference_counts.items():
                    label = label_map.get(pref, pref)
                    percentage = (count / total_users) * 100
                    st.write(f"**{label}**: {count:,}명 ({percentage:.1f}%)")
            else:
                st.info("정치 성향 데이터가 없습니다.")
    
    except FileNotFoundError as e:
        st.error("📁 데이터 파일을 찾을 수 없습니다")
        st.info("data 폴더에 prod.users.json 파일이 있는지 확인해주세요.")
        logging.error(f"File not found in overall preference page: {e}")
    except PermissionError as e:
        st.error("🔒 데이터 파일에 접근할 수 없습니다")
        st.info("파일 권한을 확인해주세요.")
        logging.error(f"Permission error in overall preference page: {e}")
    except Exception as e:
        st.error("❌ 예상치 못한 오류가 발생했습니다")
        st.info("페이지를 새로고침하거나 다른 페이지를 시도해보세요.")
        logging.error(f"Error in overall preference page: {e}", exc_info=True)
        
        # Show detailed error in expander for debugging
        with st.expander("🔍 상세 오류 정보 (개발자용)"):
            st.code(str(e))


# Alias for backward compatibility
show_overall_preference_page = show


if __name__ == "__main__":
    show()
