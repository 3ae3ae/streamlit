# Requirements Document

## Introduction

이 문서는 정치 성향 분류 기능이 있는 뉴스 앱의 MongoDB 데이터를 시각화하는 웹 애플리케이션의 요구사항을 정의합니다. 이 시스템은 다운로드된 JSON 데이터를 사용하여 사용자 정치 성향, 토픽 구독, 이슈 평가, 언론사 지지도 등을 인터랙티브하게 시각화합니다.

## Glossary

- **Visualization_System**: MongoDB 데이터를 시각화하는 Python 웹 애플리케이션
- **Political_Preference**: 사용자의 정치 성향 (left, center_left, center, center_right, right)
- **Political_Score**: 카테고리별 정치 성향 점수 (left, center, right 각각 0-100)
- **Category**: 뉴스 카테고리 (politics, economy, society, culture, technology, international)
- **Issue**: 뉴스 이슈 항목
- **Topic**: 뉴스 토픽 항목
- **Media_Source**: 언론사 정보
- **User_Evaluation**: 사용자가 이슈나 언론사에 대해 평가한 정치 성향
- **JSON_Data**: data 폴더에 저장된 MongoDB 컬렉션의 다운로드된 데이터
- **Interactive_Visualization**: 사용자가 클릭, 입력, 필터링 등으로 상호작용할 수 있는 시각화

## Requirements

### Requirement 1

**User Story:** 개발자로서, Python 웹 애플리케이션을 통해 MongoDB 데이터를 시각화하고 싶습니다. 이를 통해 실제 데이터베이스에 접근하지 않고도 데이터를 분석할 수 있습니다.

#### Acceptance Criteria

1. THE Visualization_System SHALL load JSON_Data from the data folder without connecting to MongoDB
2. THE Visualization_System SHALL use Python as the primary programming language
3. THE Visualization_System SHALL use uv as the package manager
4. THE Visualization_System SHALL provide a web-based user interface
5. THE Visualization_System SHALL parse MongoDB JSON export format including $oid and $date fields

### Requirement 2

**User Story:** 데이터 분석가로서, 전체 사용자의 정치 성향 분포를 한눈에 보고 싶습니다. 이를 통해 사용자 베이스의 정치적 균형을 파악할 수 있습니다.

#### Acceptance Criteria

1. THE Visualization_System SHALL display a pie chart showing the distribution of Political_Preference across all users
2. THE Visualization_System SHALL calculate percentages for each Political_Preference category (left, center_left, center, center_right, right)
3. THE Visualization_System SHALL load user data from prod.users.json file
4. THE Visualization_System SHALL handle users with empty or null Political_Preference values by categorizing them separately

### Requirement 3

**User Story:** 데이터 분석가로서, 시간에 따른 정치 성향 변화를 추적하고 싶습니다. 이를 통해 사용자들의 정치 성향이 어떻게 변화하는지 이해할 수 있습니다.

#### Acceptance Criteria

1. THE Visualization_System SHALL display time-series graphs of Political_Score changes using prod.userPoliticalScoreHistory.json
2. THE Visualization_System SHALL provide a filter to view data for the last 7 days with daily intervals
3. THE Visualization_System SHALL provide a filter to view data for the last 30 days with daily intervals
4. THE Visualization_System SHALL display category-specific Political_Score graphs for each Category
5. THE Visualization_System SHALL display average Political_Score graphs across all categories
6. THE Visualization_System SHALL aggregate Political_Score values by date to calculate daily proportions
7. THE Visualization_System SHALL exclude data from prod.userPoliticalPreferenceDetailHistory.json as it is deprecated

### Requirement 4

**User Story:** 콘텐츠 관리자로서, 인기 있는 토픽을 시각적으로 파악하고 싶습니다. 이를 통해 사용자들이 관심 있는 주제를 빠르게 식별할 수 있습니다.

#### Acceptance Criteria

1. THE Visualization_System SHALL display a word cloud of the top N topics based on subscriber count
2. THE Visualization_System SHALL calculate subscriber count by aggregating prod.userTopicSubscriptions.json
3. THE Visualization_System SHALL allow users to specify the number N of top topics to display
4. THE Visualization_System SHALL retrieve topic names from prod.topics.json
5. THE Visualization_System SHALL scale word sizes proportionally to subscriber counts

### Requirement 5

**User Story:** 데이터 분석가로서, 개별 사용자의 정치 성향 변화를 추적하고 싶습니다. 이를 통해 특정 사용자의 정치적 여정을 이해할 수 있습니다.

#### Acceptance Criteria

1. THE Visualization_System SHALL accept a user ID as input through a text field
2. WHEN a user ID is provided, THE Visualization_System SHALL display a time-series graph of that user's Political_Score history
3. THE Visualization_System SHALL load individual user history from prod.userPoliticalScoreHistory.json
4. THE Visualization_System SHALL display Political_Score changes for all six categories
5. IF the user ID does not exist, THEN THE Visualization_System SHALL display an error message

### Requirement 6

**User Story:** 미디어 분석가로서, 각 언론사의 지지도 변화를 추적하고 싶습니다. 이를 통해 언론사별 신뢰도와 영향력을 평가할 수 있습니다.

#### Acceptance Criteria

1. THE Visualization_System SHALL calculate Media_Source support scores based on User_Evaluation data from prod.userIssueEvaluations.json
2. WHEN a user agrees with a specific Political_Preference on an Issue, THE Visualization_System SHALL attribute support to Media_Sources of that Political_Preference covering the Issue
3. THE Visualization_System SHALL display cumulative support graphs for each Media_Source over time
4. THE Visualization_System SHALL allow users to select a Media_Source through a clickable interface
5. THE Visualization_System SHALL cross-reference prod.issues.json for Issue sources and prod.mediaSources.json for Media_Source information

### Requirement 7

**User Story:** 콘텐츠 관리자로서, 특정 이슈에 대한 사용자 지지 분포를 보고 싶습니다. 이를 통해 이슈의 정치적 반응을 이해할 수 있습니다.

#### Acceptance Criteria

1. THE Visualization_System SHALL accept an Issue ID as input through a text field
2. THE Visualization_System SHALL display a list of recent issues that users can click to select
3. WHEN an Issue is selected, THE Visualization_System SHALL display a pie chart showing the distribution of User_Evaluation perspectives (left, center, right)
4. THE Visualization_System SHALL load evaluation data from prod.userIssueEvaluations.json
5. THE Visualization_System SHALL load issue information from prod.issues.json
6. IF the Issue ID does not exist, THEN THE Visualization_System SHALL display an error message

### Requirement 8

**User Story:** 사용자로서, 미려하고 인터랙티브한 시각화를 경험하고 싶습니다. 이를 통해 데이터를 더 쉽게 이해하고 탐색할 수 있습니다.

#### Acceptance Criteria

1. THE Visualization_System SHALL use modern Python visualization libraries for Interactive_Visualization
2. THE Visualization_System SHALL provide hover tooltips showing detailed information on chart elements
3. THE Visualization_System SHALL allow users to zoom and pan on time-series graphs
4. THE Visualization_System SHALL use a consistent and professional color scheme across all visualizations
5. THE Visualization_System SHALL provide smooth transitions and animations when updating visualizations
6. THE Visualization_System SHALL ensure all visualizations are responsive and render correctly on different screen sizes

### Requirement 9

**User Story:** 개발자로서, 애플리케이션을 쉽게 실행하고 관리하고 싶습니다. 이를 통해 개발 및 배포 프로세스를 간소화할 수 있습니다.

#### Acceptance Criteria

1. THE Visualization_System SHALL use uv for dependency management
2. THE Visualization_System SHALL provide a pyproject.toml file with all required dependencies
3. THE Visualization_System SHALL include clear instructions for running the application
4. THE Visualization_System SHALL start the web server with a single command
5. THE Visualization_System SHALL handle missing or corrupted JSON_Data files gracefully with error messages

### Requirement 10

**User Story:** 데이터 분석가로서, 차트의 시각적 품질과 인터랙티브 기능이 향상되기를 원합니다. 이를 통해 데이터를 더 명확하고 직관적으로 이해할 수 있습니다.

#### Acceptance Criteria

1. THE Visualization_System SHALL render all charts and graphs with smooth animations and transitions
2. THE Visualization_System SHALL use modern, visually appealing design elements for all visualizations
3. THE Visualization_System SHALL provide enhanced hover interactions with detailed tooltips
4. THE Visualization_System SHALL support interactive legends that allow toggling data series visibility
5. THE Visualization_System SHALL use gradient colors and modern styling to improve visual aesthetics

### Requirement 11

**User Story:** 데이터 분석가로서, 차트의 축 범위와 배율이 데이터 변화를 효과적으로 보여주기를 원합니다. 이를 통해 미세한 데이터 변화도 명확하게 파악할 수 있습니다.

#### Acceptance Criteria

1. WHEN displaying time-series data, THE Visualization_System SHALL automatically adjust y-axis range to fit the data range with appropriate padding
2. THE Visualization_System SHALL calculate optimal y-axis intervals based on data variance
3. THE Visualization_System SHALL use dynamic scaling that emphasizes data changes rather than absolute values
4. WHEN data variance is small, THE Visualization_System SHALL zoom into the relevant range to make changes visible
5. THE Visualization_System SHALL provide manual axis range controls for user customization

### Requirement 12

**User Story:** 사용자로서, 메인 페이지 외의 모든 페이지에서도 시각화가 정상적으로 표시되기를 원합니다. 이를 통해 모든 기능을 문제없이 사용할 수 있습니다.

#### Acceptance Criteria

1. THE Visualization_System SHALL display visualizations correctly on all navigation pages
2. THE Visualization_System SHALL load required data for each page without errors
3. THE Visualization_System SHALL handle page-specific errors gracefully with informative messages
4. THE Visualization_System SHALL ensure consistent layout and styling across all pages
5. THE Visualization_System SHALL validate that all page modules are properly integrated with the main application

### Requirement 13

**User Story:** 미디어 분석가로서, 여러 언론사의 지지도를 한 차트에서 동시에 비교하고 싶습니다. 이를 통해 언론사 간 상대적 지지도 변화를 쉽게 파악할 수 있습니다.

#### Acceptance Criteria

1. THE Visualization_System SHALL provide an option to display multiple Media_Source support trends on a single chart
2. THE Visualization_System SHALL allow users to select multiple Media_Sources through checkboxes or multi-select interface
3. THE Visualization_System SHALL use distinct colors for each Media_Source line in the combined chart
4. THE Visualization_System SHALL provide a legend that identifies each Media_Source by name and color
5. THE Visualization_System SHALL maintain chart readability when displaying multiple data series

### Requirement 14

**User Story:** 사용자로서, ID를 수동으로 입력하지 않고 클릭만으로 항목을 선택하고 자동으로 시각화가 업데이트되기를 원합니다. 이를 통해 더 빠르고 편리하게 데이터를 탐색할 수 있습니다.

#### Acceptance Criteria

1. WHEN a user clicks on a selectable item (Issue, Media_Source, User), THE Visualization_System SHALL automatically update the visualization without requiring manual ID input
2. THE Visualization_System SHALL provide clickable lists or buttons for all selectable entities
3. THE Visualization_System SHALL highlight the currently selected item in the selection interface
4. THE Visualization_System SHALL update the visualization immediately upon selection
5. THE Visualization_System SHALL maintain the manual ID input option as an alternative selection method
