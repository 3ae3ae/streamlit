"""
Popular topics word cloud page.
Displays a word cloud visualization of the most popular topics by subscriber count.
"""

import logging
import streamlit as st

from data_loader import load_topics, load_topic_subscriptions
from visualizations.wordcloud import create_topic_wordcloud


def show():
    """
    Display the popular topics word cloud page.
    
    This page shows a word cloud where word size is proportional to the number
    of subscribers for each topic. Users can specify how many top topics to display.
    """
    st.title("인기 토픽 워드클라우드")
    st.markdown("구독자 수가 많은 인기 토픽을 워드클라우드로 시각화합니다.")
    
    try:
        # Load data
        with st.spinner("토픽 데이터를 로드하는 중..."):
            topics_df = load_topics()
            subscriptions_df = load_topic_subscriptions()
        
        if topics_df.empty:
            st.warning("토픽 데이터가 없습니다.")
            return
        
        if subscriptions_df.empty:
            st.warning("토픽 구독 데이터가 없습니다.")
            return
        
        # Sidebar controls
        st.sidebar.header("워드클라우드 설정")
        
        # Top N topics input
        top_n = st.sidebar.number_input(
            "상위 토픽 수",
            min_value=10,
            max_value=200,
            value=50,
            step=10,
            help="워드클라우드에 표시할 상위 토픽의 개수를 선택하세요"
        )
        
        # Color scheme selection
        colormap_options = {
            "기본 (Viridis)": "viridis",
            "따뜻한 색상 (Plasma)": "plasma",
            "차가운 색상 (Cool)": "cool",
            "무지개 (Rainbow)": "rainbow",
            "파스텔 (Pastel1)": "Pastel1"
        }
        
        colormap_label = st.sidebar.selectbox(
            "색상 테마",
            options=list(colormap_options.keys()),
            index=0
        )
        
        colormap = colormap_options[colormap_label]
        
        # Generate word cloud
        with st.spinner(f"상위 {top_n}개 토픽의 워드클라우드를 생성하는 중..."):
            wordcloud_image = create_topic_wordcloud(
                topics_df,
                subscriptions_df,
                top_n=int(top_n),
                width=1200,
                height=600,
                colormap=colormap
            )
        
        if wordcloud_image is None:
            st.error("워드클라우드를 생성할 수 없습니다. 데이터를 확인해주세요.")
            return
        
        # Display word cloud
        st.image(wordcloud_image, use_container_width=True)
        
        # Display statistics
        from processing.aggregators import calculate_topic_subscriber_counts
        
        topic_counts = calculate_topic_subscriber_counts(topics_df, subscriptions_df)
        
        if not topic_counts.empty:
            top_topics = topic_counts.head(int(top_n))
            
            col1, col2, col3 = st.columns(3)
            col1.metric("전체 토픽 수", f"{len(topics_df):,}")
            col2.metric("전체 구독 수", f"{len(subscriptions_df):,}")
            col3.metric("표시된 토픽 수", f"{len(top_topics):,}")
            
            # Display top topics table
            with st.expander("상위 토픽 목록"):
                st.markdown(f"### 상위 {min(10, len(top_topics))}개 토픽")
                
                display_topics = top_topics.head(10)
                
                for idx, row in display_topics.iterrows():
                    topic_name = row["topic_name"]
                    subscriber_count = row["subscriber_count"]
                    st.write(f"**{idx + 1}. {topic_name}**: {subscriber_count:,}명")
        
        # Display usage information
        with st.expander("워드클라우드 설명"):
            st.markdown("""
            ### 워드클라우드란?
            워드클라우드는 단어의 빈도나 중요도를 시각적으로 표현하는 방법입니다.
            이 페이지에서는 각 토픽의 구독자 수에 비례하여 단어 크기가 결정됩니다.
            
            ### 해석 방법
            - **큰 글씨**: 구독자가 많은 인기 토픽
            - **작은 글씨**: 상대적으로 구독자가 적은 토픽
            - **색상**: 선택한 색상 테마에 따라 다양하게 표현됩니다
            
            ### 사용 팁
            - 상위 토픽 수를 조정하여 더 많거나 적은 토픽을 표시할 수 있습니다
            - 색상 테마를 변경하여 다양한 시각적 효과를 경험할 수 있습니다
            - 상위 토픽 목록을 펼쳐서 정확한 구독자 수를 확인할 수 있습니다
            """)
    
    except FileNotFoundError as e:
        st.error("📁 데이터 파일을 찾을 수 없습니다")
        st.info("data 폴더에 prod.topics.json 및 prod.userTopicSubscriptions.json 파일이 있는지 확인해주세요.")
        logging.error(f"File not found in topic wordcloud page: {e}")
    except PermissionError as e:
        st.error("🔒 데이터 파일에 접근할 수 없습니다")
        st.info("파일 권한을 확인해주세요.")
        logging.error(f"Permission error in topic wordcloud page: {e}")
    except Exception as e:
        st.error("❌ 예상치 못한 오류가 발생했습니다")
        st.info("페이지를 새로고침하거나 다른 페이지를 시도해보세요.")
        logging.error(f"Error in topic wordcloud page: {e}", exc_info=True)
        
        # Show detailed error in expander for debugging
        with st.expander("🔍 상세 오류 정보 (개발자용)"):
            st.code(str(e))


# Alias for backward compatibility
show_topic_wordcloud_page = show


if __name__ == "__main__":
    show()
