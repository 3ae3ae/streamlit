"""
Issue evaluation distribution page.
Displays pie charts showing the distribution of user evaluations for specific issues.
"""

import logging
import streamlit as st

from data_loader import load_issue_evaluations, load_issues
from processing.aggregators import get_recent_issues
from visualizations.charts import create_issue_evaluation_pie_chart


def show():
    """
    Display the issue evaluation distribution page.
    
    This page shows a pie chart of evaluation distribution for a specific issue,
    with an input field for issue ID and a clickable list of recent issues.
    """
    st.title("이슈 평가 분포")
    st.markdown("특정 이슈에 대한 사용자 평가 분포를 확인할 수 있습니다.")
    
    try:
        # Load data
        with st.spinner("데이터를 로드하는 중..."):
            evaluations_df = load_issue_evaluations()
            issues_df = load_issues()
        
        if evaluations_df.empty:
            st.warning("이슈 평가 데이터가 없습니다.")
            return
        
        if issues_df.empty:
            st.warning("이슈 데이터가 없습니다.")
            return
        
        # Get recent issues
        recent_issues = get_recent_issues(issues_df, limit=20)
        
        # Initialize session state for selected issue
        if "selected_issue_id" not in st.session_state:
            st.session_state.selected_issue_id = None
        
        # Issue ID input
        st.markdown("### 이슈 ID 입력")
        manual_issue_id = st.text_input(
            "이슈 ID",
            value=st.session_state.selected_issue_id if st.session_state.selected_issue_id else "",
            placeholder="이슈 ID를 입력하세요",
            help="평가 분포를 확인하고 싶은 이슈의 ID를 입력하세요"
        )
        
        # Update session state if manual input is provided
        if manual_issue_id and manual_issue_id != st.session_state.selected_issue_id:
            st.session_state.selected_issue_id = manual_issue_id
        
        # Display recent issues as clickable list
        st.markdown("### 최근 이슈 목록")
        st.info("아래 목록에서 이슈를 클릭하여 선택할 수 있습니다.")
        
        if not recent_issues.empty:
            # Create a container for recent issues
            with st.container():
                for idx, (_, issue) in enumerate(recent_issues.iterrows(), 1):
                    issue_id_val = issue.get("_id", "")
                    issue_title = issue.get("title", "제목 없음")
                    
                    # Truncate long titles
                    if len(issue_title) > 100:
                        issue_title = issue_title[:100] + "..."
                    
                    # Get evaluation count for this issue
                    eval_count = len(evaluations_df[evaluations_df["issueId"] == issue_id_val])
                    
                    # Check if this issue is currently selected
                    is_selected = (st.session_state.selected_issue_id == issue_id_val)
                    
                    # Display issue with button
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        # Use different button type for selected issue
                        button_type = "primary" if is_selected else "secondary"
                        if st.button(
                            f"{'✓ ' if is_selected else ''}{idx}. {issue_title}",
                            key=f"issue_{issue_id_val}",
                            help=f"이슈 ID: {issue_id_val}",
                            type=button_type
                        ):
                            st.session_state.selected_issue_id = issue_id_val
                            st.rerun()
                    
                    with col2:
                        st.caption(f"평가 {eval_count}개")
                    
                    # Add separator
                    if idx < len(recent_issues):
                        st.divider()
        else:
            st.warning("최근 이슈 데이터가 없습니다.")
        
        # Use the selected issue ID from session state
        issue_id = st.session_state.selected_issue_id
        
        # Process and display chart if issue ID is provided
        if issue_id:
            # Check if issue exists
            issue_data = issues_df[issues_df["_id"] == issue_id]
            
            if issue_data.empty:
                st.error(f"❌ 이슈 ID '{issue_id}'에 대한 데이터를 찾을 수 없습니다.")
                st.info("위의 '최근 이슈 목록'에서 유효한 이슈를 선택하거나, 올바른 이슈 ID를 입력하세요.")
                return
            
            # Get issue details
            issue = issue_data.iloc[0]
            issue_title = issue.get("title", "제목 없음")
            
            st.success(f"✅ 이슈를 찾았습니다: {issue_title}")
            
            # Check if there are evaluations for this issue
            issue_evaluations = evaluations_df[evaluations_df["issueId"] == issue_id]
            
            if issue_evaluations.empty:
                st.warning(f"이슈 '{issue_title}'에 대한 평가 데이터가 없습니다.")
                return
            
            # Display statistics
            col1, col2, col3 = st.columns(3)
            
            total_evaluations = len(issue_evaluations)
            col1.metric("총 평가 수", f"{total_evaluations:,}")
            
            if "perspective" in issue_evaluations.columns:
                perspective_counts = issue_evaluations["perspective"].value_counts()
                
                left_count = perspective_counts.get("left", 0)
                center_count = perspective_counts.get("center", 0)
                right_count = perspective_counts.get("right", 0)
                
                col2.metric("진보 평가", f"{left_count:,}")
                col3.metric("보수 평가", f"{right_count:,}")
            
            # Display issue details
            with st.expander("이슈 상세 정보"):
                st.markdown(f"**제목**: {issue_title}")
                st.markdown(f"**이슈 ID**: {issue_id}")
                
                if "createdAt" in issue.index and issue["createdAt"] is not None:
                    st.markdown(f"**생성일**: {issue['createdAt'].strftime('%Y-%m-%d %H:%M:%S')}")
                
                if "category" in issue.index:
                    category_map = {
                        "politics": "정치",
                        "economy": "경제",
                        "society": "사회",
                        "culture": "문화",
                        "technology": "기술",
                        "international": "국제"
                    }
                    category_label = category_map.get(issue["category"], issue["category"])
                    st.markdown(f"**카테고리**: {category_label}")
                
                if "description" in issue.index and issue["description"]:
                    st.markdown(f"**설명**: {issue['description']}")
            
            # Create and display pie chart
            with st.spinner("차트를 생성하는 중..."):
                fig = create_issue_evaluation_pie_chart(evaluations_df, issue_id)
            
            st.plotly_chart(fig, width="stretch")
            
            # Display additional information
            with st.expander("평가 분포 해석"):
                st.markdown("""
                ### 평가 성향 설명
                사용자들이 이 이슈에 대해 어떤 정치적 관점에서 동의했는지를 보여줍니다.
                
                - **진보**: 진보적 관점에서 이슈에 동의한 사용자 수
                - **중도**: 중도적 관점에서 이슈에 동의한 사용자 수
                - **보수**: 보수적 관점에서 이슈에 동의한 사용자 수
                
                ### 차트 해석
                - 특정 성향이 크게 나타나면 해당 이슈가 그 성향의 사용자들에게 더 많은 지지를 받았음을 의미
                - 균형잡힌 분포는 이슈가 다양한 정치 성향의 사용자들에게 공감을 얻었음을 의미
                - 한쪽으로 치우친 분포는 이슈가 특정 정치 성향과 강하게 연관되어 있음을 의미
                """)
            
            # Display evaluation details
            with st.expander("평가 상세 내역"):
                if "perspective" in issue_evaluations.columns:
                    st.markdown("### 성향별 평가 수")
                    
                    perspective_map = {
                        "left": "진보",
                        "center": "중도",
                        "right": "보수"
                    }
                    
                    for perspective, label in perspective_map.items():
                        count = len(issue_evaluations[issue_evaluations["perspective"] == perspective])
                        percentage = (count / total_evaluations * 100) if total_evaluations > 0 else 0
                        st.write(f"**{label}**: {count:,}개 ({percentage:.1f}%)")
                
                # Show recent evaluations
                st.markdown("### 최근 평가 (최대 10개)")
                
                recent_evals = issue_evaluations.sort_values("evaluatedAt", ascending=False).head(10) if "evaluatedAt" in issue_evaluations.columns else issue_evaluations.head(10)
                
                for idx, (_, evaluation) in enumerate(recent_evals.iterrows(), 1):
                    perspective = evaluation.get("perspective", "unknown")
                    perspective_label = {
                        "left": "진보",
                        "center": "중도",
                        "right": "보수"
                    }.get(perspective, perspective)
                    
                    eval_date = ""
                    if "evaluatedAt" in evaluation.index and evaluation["evaluatedAt"] is not None:
                        eval_date = f" - {evaluation['evaluatedAt'].strftime('%Y-%m-%d %H:%M')}"
                    
                    st.write(f"{idx}. {perspective_label}{eval_date}")
        else:
            st.info("👆 위의 입력 필드에 이슈 ID를 입력하거나, 최근 이슈 목록에서 선택하여 평가 분포를 확인하세요.")
    
    except FileNotFoundError as e:
        st.error("📁 데이터 파일을 찾을 수 없습니다")
        st.info("data 폴더에 prod.userIssueEvaluations.json 및 prod.issues.json 파일이 있는지 확인해주세요.")
        logging.error(f"File not found in issue evaluation page: {e}")
    except PermissionError as e:
        st.error("🔒 데이터 파일에 접근할 수 없습니다")
        st.info("파일 권한을 확인해주세요.")
        logging.error(f"Permission error in issue evaluation page: {e}")
    except Exception as e:
        st.error("❌ 예상치 못한 오류가 발생했습니다")
        st.info("페이지를 새로고침하거나 다른 페이지를 시도해보세요.")
        logging.error(f"Error in issue evaluation page: {e}", exc_info=True)
        
        # Show detailed error in expander for debugging
        with st.expander("🔍 상세 오류 정보 (개발자용)"):
            st.code(str(e))


# Alias for backward compatibility
show_issue_evaluation_page = show


if __name__ == "__main__":
    show()
