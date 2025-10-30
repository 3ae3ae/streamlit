# Implementation Plan

- [x] 1. 프로젝트 구조 및 의존성 설정

  - pyproject.toml에 필요한 패키지 추가 (streamlit, plotly, pandas, wordcloud, pillow)
  - 디렉토리 구조 생성 (pages/, visualizations/, processing/)
  - _Requirements: 1.2, 1.3, 9.1, 9.2_

- [x] 2. 데이터 로더 모듈 구현

  - [x] 2.1 기본 JSON 로더 함수 작성

    - data_loader.py 파일 생성
    - MongoDB export 형식 파싱 함수 구현 (parse_mongodb_date, parse_mongodb_oid)
    - 에러 핸들링 추가 (파일 없음, 파싱 오류)
    - _Requirements: 1.1, 1.5, 9.5_

  - [x] 2.2 각 컬렉션별 로더 함수 구현
    - load_users() 함수 구현 및 캐싱
    - load_political_score_history() 함수 구현 및 캐싱
    - load_topics() 및 load_topic_subscriptions() 함수 구현
    - load_issues(), load_issue_evaluations(), load_media_sources() 함수 구현
    - _Requirements: 2.3, 3.1, 4.2, 5.3, 6.1, 7.4_

- [x] 3. 데이터 집계 모듈 구현

  - [x] 3.1 정치 성향 집계 함수 작성

    - processing/aggregators.py 파일 생성
    - aggregate_political_scores_by_date() 함수 구현
    - 날짜별 점수 합산 및 비율 계산 로직
    - _Requirements: 3.6_

  - [x] 3.2 토픽 및 언론사 집계 함수 작성
    - calculate_topic_subscriber_counts() 함수 구현
    - calculate_media_support_scores() 함수 구현 (이슈 평가 기반 지지도 계산)
    - get_recent_issues() 함수 구현
    - _Requirements: 4.2, 6.1, 6.2, 7.2_

- [x] 4. 차트 생성 모듈 구현

  - [x] 4.1 기본 차트 테마 및 유틸리티 작성

    - visualizations/charts.py 파일 생성
    - apply_chart_theme() 함수로 일관된 스타일 적용
    - 한글 폰트 설정 및 색상 팔레트 정의
    - _Requirements: 8.4, 8.5_

  - [x] 4.2 정치 성향 관련 차트 함수 작성

    - create_political_preference_pie_chart() 구현 (전체 성향 분포)
    - create_time_series_chart() 구현 (시간별 성향 변화)
    - create_user_political_journey_chart() 구현 (개인 성향 변화)
    - 호버 툴팁, 줌/팬 기능 추가
    - _Requirements: 2.1, 2.2, 3.2, 3.3, 3.4, 3.5, 5.2, 5.4, 8.2, 8.3_

  - [x] 4.3 이슈 및 언론사 차트 함수 작성
    - create_media_support_chart() 구현 (언론사 지지도)
    - create_issue_evaluation_pie_chart() 구현 (이슈 평가 분포)
    - _Requirements: 6.3, 7.3_

- [x] 5. 워드클라우드 생성 모듈 구현

  - visualizations/wordcloud.py 파일 생성
  - create_topic_wordcloud() 함수 구현
  - 구독자 수 기반 단어 크기 조정
  - 한글 폰트 설정
  - _Requirements: 4.1, 4.3, 4.4, 4.5_

- [x] 6. 페이지 모듈 구현

  - [x] 6.1 전체 성향 분포 페이지

    - pages/overall_preference.py 파일 생성
    - 사용자 데이터 로드 및 원 그래프 표시
    - 빈 값 처리 로직
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

  - [x] 6.2 시간별 성향 변화 페이지

    - pages/time_series.py 파일 생성
    - 날짜 범위 필터 (7일/30일) 구현
    - 카테고리별/평균 보기 토글
    - 카테고리 선택 드롭다운
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_

  - [x] 6.3 인기 토픽 워드클라우드 페이지

    - pages/topic_wordcloud.py 파일 생성
    - 상위 N개 토픽 수 입력 위젯
    - 워드클라우드 표시
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [x] 6.4 개인 성향 변화 페이지

    - pages/user_journey.py 파일 생성
    - 사용자 ID 입력 필드
    - 존재하지 않는 ID 에러 처리
    - 6개 카테고리 점수 그래프 표시
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

  - [x] 6.5 언론사 지지도 페이지

    - pages/media_support.py 파일 생성
    - 언론사 선택 UI (클릭 가능한 목록)
    - 누적 지지도 그래프 표시
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

  - [x] 6.6 이슈 평가 분포 페이지
    - pages/issue_evaluation.py 파일 생성
    - 이슈 ID 입력 필드
    - 최근 이슈 클릭 가능한 목록
    - 평가 분포 원 그래프 표시
    - 존재하지 않는 ID 에러 처리
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_

- [x] 7. 메인 애플리케이션 구현

  - app.py 파일 생성
  - Streamlit 페이지 설정 (제목, 아이콘, 레이아웃)
  - 사이드바 네비게이션 구현
  - 페이지 라우팅 로직
  - _Requirements: 1.4, 8.6, 9.4_

- [x] 8. 에러 핸들링 및 사용자 피드백 개선

  - 모든 페이지에 try-catch 블록 추가
  - 데이터 없음 경고 메시지
  - 로딩 스피너 추가
  - _Requirements: 9.5_

- [x] 9. README 및 실행 가이드 작성

  - README.md 업데이트
  - 설치 및 실행 방법 문서화
  - 데이터 파일 요구사항 명시
  - _Requirements: 9.3, 9.4_

- [ ]\* 10. 차트 시각적 품질 및 인터랙티브 기능 향상

  - [ ]\* 10.1 향상된 차트 테마 함수 구현

    - visualizations/charts.py에 apply_enhanced_theme() 함수 추가
    - Plotly template을 'plotly_white'로 설정
    - 애니메이션 효과 추가 (transition_duration=500)
    - 향상된 호버 모드 설정 (hovermode='x unified')
    - 인터랙티브 범례 설정 (itemclick='toggle')
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

  - [ ]\* 10.2 모든 차트 함수에 향상된 테마 적용
    - 기존 모든 차트 생성 함수에 apply_enhanced_theme() 적용
    - 그라디언트 색상 및 모던 스타일링 추가
    - 부드러운 전환 효과 확인
    - _Requirements: 10.1, 10.2, 10.5_

- [x] 11. 동적 축 스케일링 구현

  - [x] 11.1 최적 Y축 범위 계산 함수 구현

    - visualizations/charts.py에 calculate_optimal_y_range() 함수 추가
    - 데이터의 min/max 기반 범위 계산
    - 10% padding 추가로 여백 확보
    - 작은 변화도 보이도록 확대된 범위 사용
    - _Requirements: 11.1, 11.2, 11.3, 11.4_

  - [x] 11.2 모든 시계열 차트에 동적 스케일링 적용
    - create_time_series_chart()에 동적 y축 범위 적용
    - create_user_political_journey_chart()에 동적 y축 범위 적용
    - create_media_support_chart()에 동적 y축 범위 적용
    - 수동 조정 가능하도록 fixedrange=False 설정
    - _Requirements: 11.1, 11.4, 11.5_

- [x] 12. 모든 페이지 통합 및 수정

  - [x] 12.1 main.py 구조 개선

    - 모든 페이지 모듈을 올바르게 import
    - 페이지 함수 딕셔너리 구조로 라우팅 개선
    - 각 페이지가 show() 함수를 export하도록 확인
    - _Requirements: 12.1, 12.5_

  - [x] 12.2 각 페이지 모듈 수정
    - 각 페이지에 show() 함수 추가 (진입점)
    - 페이지별 독립적인 데이터 로딩 및 에러 처리
    - 일관된 레이아웃 및 스타일 적용
    - 페이지별 에러 메시지 개선
    - _Requirements: 12.2, 12.3, 12.4_

- [x] 13. 다중 언론사 비교 기능 구현

  - [x] 13.1 다중 언론사 지지도 차트 함수 수정

    - create_media_support_chart()에 media_ids 파라미터 추가
    - 여러 언론사 데이터를 한 차트에 표시
    - 각 언론사별 구분된 색상 사용
    - 범례로 언론사 식별 가능하도록 구현
    - _Requirements: 13.1, 13.3, 13.4, 13.5_

  - [x] 13.2 언론사 지지도 페이지 UI 개선
    - pages/media_support.py에 multiselect 위젯 추가
    - 단일/다중 보기 모드 전환 기능
    - 최대 7개 언론사 선택 제한
    - 선택된 언론사 목록 표시
    - _Requirements: 13.2, 13.5_

- [x] 14. 클릭으로 자동 선택 기능 구현

  - [x] 14.1 이슈 평가 페이지에 클릭 선택 추가

    - pages/issue_evaluation.py에 클릭 가능한 이슈 목록 추가
    - st.button() 또는 st.radio()로 이슈 선택 UI 구현
    - 선택 시 자동으로 차트 업데이트
    - 현재 선택된 이슈 하이라이트 표시
    - 수동 ID 입력 옵션 유지
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_

  - [x] 14.2 언론사 지지도 페이지에 클릭 선택 추가

    - pages/media_support.py에 클릭 가능한 언론사 목록 추가
    - 선택 시 자동으로 차트 업데이트
    - 현재 선택된 언론사 하이라이트 표시
    - _Requirements: 14.1, 14.2, 14.3, 14.4_

  - [x] 14.3 개인 성향 변화 페이지에 클릭 선택 추가
    - pages/user_journey.py에 사용자 선택 UI 개선
    - 최근 활동 사용자 목록 표시 (선택 가능)
    - 선택 시 자동으로 차트 업데이트
    - _Requirements: 14.1, 14.2, 14.3, 14.4_

- [ ]\* 15. 테스트 작성

  - [ ]\* 15.1 데이터 로더 유닛 테스트

    - test_data_loader.py 파일 생성
    - MongoDB 형식 파싱 테스트
    - 샘플 데이터로 로더 함수 테스트
    - _Requirements: 1.5_

  - [ ]\* 15.2 집계 함수 유닛 테스트
    - test_aggregators.py 파일 생성
    - 점수 집계 로직 테스트
    - 지지도 계산 로직 테스트
    - _Requirements: 3.6, 6.2_
