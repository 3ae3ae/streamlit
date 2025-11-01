# MongoDB 데이터 시각화 도구

정치 성향 분류 기능이 있는 뉴스 앱의 MongoDB 데이터를 시각화하는 인터랙티브 웹 애플리케이션입니다. Streamlit과 Plotly를 사용하여 사용자 정치 성향, 토픽 구독, 이슈 평가, 언론사 지지도 등을 미려하게 시각화합니다.

## 주요 기능

### 📊 시각화 페이지

1. **전체 성향 분포**
   - 모든 사용자의 정치 성향 분포를 원 그래프로 표시
   - 진보, 중도좌파, 중도, 중도우파, 보수 비율 확인

2. **시간별 성향 변화**
   - 시간에 따른 정치 성향 점수 변화 추적
   - 7일/30일 기간 선택 가능
   - 카테고리별 또는 평균 보기 지원
   - 6개 뉴스 카테고리 (정치, 경제, 사회, 문화, 기술, 국제)

3. **인기 토픽 워드클라우드**
   - 구독자 수 기반 인기 토픽 시각화
   - 상위 N개 토픽 수 조정 가능
   - 구독자 수에 비례한 단어 크기

4. **개인 성향 변화**
   - 특정 사용자의 정치 성향 변화 추적
   - 6개 카테고리별 점수 그래프
   - 사용자 ID 입력으로 조회

5. **언론사 지지도**
   - 사용자 평가 기반 언론사 누적 지지도
   - 언론사 선택 및 시간별 변화 확인
   - 정치 성향별 지지도 분석

6. **이슈 평가 분포**
   - 특정 이슈에 대한 사용자 평가 분포
   - 최근 이슈 목록 제공
   - 진보/중도/보수 평가 비율 원 그래프

### ✨ 인터랙티브 기능

- 📈 줌/팬 기능이 있는 차트
- 🖱️ 호버 툴팁으로 상세 정보 표시
- 🎨 일관된 색상 테마 (진보: 파랑, 중도: 보라, 보수: 빨강)
- 🌙 다크모드 완벽 지원 (브라우저 설정에 따라 자동 적용)
- 📱 반응형 레이아웃
- ⚡ 빠른 데이터 캐싱

## 기술 스택

- **Web Framework**: Streamlit 1.28+
- **Visualization**: Plotly 5.17+, WordCloud 1.9+
- **Data Processing**: Pandas 2.1+
- **Package Manager**: uv
- **Language**: Python 3.12+

## 설치 방법

### 1. 사전 요구사항

- Python 3.12 이상
- uv 패키지 매니저

#### uv 설치

```bash
# macOS/Linux (Homebrew)
brew install uv

# macOS/Linux (curl)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# pip를 통한 설치
pip install uv
```

자세한 설치 방법은 [uv 공식 문서](https://docs.astral.sh/uv/getting-started/installation/)를 참조하세요.

### 2. 프로젝트 설정

```bash
# 저장소 클론 (또는 프로젝트 디렉토리로 이동)
cd mongodb-visualization-tool

# 의존성 설치
uv sync
```

이 명령은 `pyproject.toml`에 정의된 모든 패키지를 자동으로 설치합니다:
- streamlit
- plotly
- pandas
- wordcloud
- pillow
- pydantic
- pymongo

## 데이터 파일 요구사항

애플리케이션을 실행하기 전에 MongoDB에서 내보낸 JSON 파일들이 `data/` 디렉토리에 있어야 합니다.

### 필수 데이터 파일

다음 파일들이 `data/` 디렉토리에 위치해야 합니다:

```
data/
├── prod.users.json                              # 사용자 정보 및 정치 성향
├── prod.userPoliticalScoreHistory.json          # 사용자 정치 성향 점수 이력
├── prod.topics.json                             # 토픽 정보
├── prod.userTopicSubscriptions.json             # 사용자 토픽 구독 정보
├── prod.issues.json                             # 이슈 정보
├── prod.userIssueEvaluations.json               # 사용자 이슈 평가
└── prod.mediaSources.json                       # 언론사 정보
```

### 데이터 파일 형식

파일들은 MongoDB의 JSON export 형식이어야 합니다:

```json
{
  "_id": {"$oid": "507f1f77bcf86cd799439011"},
  "createdAt": {"$date": "2024-01-01T00:00:00.000Z"},
  "politicalPreference": "center",
  ...
}
```

애플리케이션은 자동으로 MongoDB 형식(`$oid`, `$date`)을 파싱합니다.

### MongoDB에서 데이터 내보내기

```bash
# 단일 컬렉션 내보내기
mongoexport --db=your_database --collection=users --out=data/prod.users.json --jsonArray

# 모든 필수 컬렉션 내보내기 스크립트 예시
collections=(
  "users"
  "userPoliticalScoreHistory"
  "topics"
  "userTopicSubscriptions"
  "issues"
  "userIssueEvaluations"
  "mediaSources"
)

for collection in "${collections[@]}"; do
  mongoexport --db=your_database --collection=$collection \
    --out=data/prod.$collection.json --jsonArray
done
```

## 실행 방법

### 로컬 개발 서버 실행

```bash
# uv를 사용하여 Streamlit 앱 실행
uv run streamlit run main.py
```

또는

```bash
# 가상환경 활성화 후 실행
source .venv/bin/activate  # macOS/Linux
# 또는
.venv\Scripts\activate     # Windows

streamlit run main.py
```

### 실행 옵션

```bash
# 특정 포트에서 실행
uv run streamlit run main.py --server.port 8080

# 브라우저 자동 열기 비활성화
uv run streamlit run main.py --server.headless true

# 파일 감시 비활성화 (프로덕션)
uv run streamlit run main.py --server.fileWatcherType none
```

### 접속

브라우저가 자동으로 열리며, 다음 주소로 접속할 수 있습니다:
```
http://localhost:8501
```

## 프로젝트 구조

```
.
├── main.py                      # 애플리케이션 진입점
├── data_loader.py               # JSON 데이터 로더 및 파서
├── pyproject.toml               # 프로젝트 설정 및 의존성
├── README.md                    # 이 문서
├── data/                        # MongoDB JSON 데이터 파일
│   ├── prod.users.json
│   ├── prod.userPoliticalScoreHistory.json
│   └── ...
├── pages/                       # Streamlit 페이지 모듈
│   ├── overall_preference.py    # 전체 성향 분포
│   ├── time_series.py           # 시간별 성향 변화
│   ├── topic_wordcloud.py       # 인기 토픽 워드클라우드
│   ├── user_journey.py          # 개인 성향 변화
│   ├── media_support.py         # 언론사 지지도
│   └── issue_evaluation.py      # 이슈 평가 분포
├── visualizations/              # 차트 및 시각화 생성
│   ├── charts.py                # Plotly 차트 생성
│   └── wordcloud.py             # 워드클라우드 생성
├── processing/                  # 데이터 처리 및 집계
│   └── aggregators.py           # 데이터 집계 함수
└── schemas/                     # 데이터 스키마 정의 (Pydantic)
    └── ...
```

## 사용 가이드

### 1. 전체 성향 분포 보기

1. 사이드바에서 "전체 성향 분포" 선택
2. 원 그래프에서 각 성향의 비율 확인
3. 호버하여 정확한 사용자 수와 비율 확인

### 2. 시간별 성향 변화 추적

1. "시간별 성향 변화" 페이지 선택
2. 기간 선택 (7일 또는 30일)
3. 보기 유형 선택:
   - **카테고리별**: 특정 뉴스 카테고리의 성향 변화
   - **평균**: 모든 카테고리의 평균 성향 변화
4. 차트에서 줌/팬으로 상세 분석

### 3. 인기 토픽 확인

1. "인기 토픽 워드클라우드" 페이지 선택
2. 표시할 토픽 수 입력 (기본값: 50)
3. 워드클라우드에서 큰 단어일수록 구독자가 많음

### 4. 개인 성향 변화 분석

1. "개인 성향 변화" 페이지 선택
2. 사용자 ID 입력
3. 6개 카테고리별 정치 성향 점수 변화 확인

### 5. 언론사 지지도 분석

1. "언론사 지지도" 페이지 선택
2. 언론사 목록에서 선택
3. 시간에 따른 누적 지지도 그래프 확인
4. 정치 성향별 지지도 비교

### 6. 이슈 평가 분포 확인

1. "이슈 평가 분포" 페이지 선택
2. 최근 이슈 목록에서 선택하거나 이슈 ID 직접 입력
3. 진보/중도/보수 평가 분포 원 그래프 확인

## 문제 해결

### 데이터 파일을 찾을 수 없습니다

**증상**: "데이터 파일을 찾을 수 없습니다" 오류 메시지

**해결 방법**:
1. `data/` 디렉토리가 존재하는지 확인
2. 필수 JSON 파일들이 올바른 이름으로 있는지 확인
3. 파일 권한 확인 (읽기 권한 필요)

### 데이터 파싱 오류

**증상**: JSON 파싱 관련 오류

**해결 방법**:
1. JSON 파일이 유효한 형식인지 확인
2. MongoDB export 형식(`--jsonArray` 옵션)으로 내보냈는지 확인
3. 파일이 손상되지 않았는지 확인

### 차트가 표시되지 않음

**증상**: 빈 페이지 또는 "데이터가 없습니다" 메시지

**해결 방법**:
1. 해당 시각화에 필요한 데이터 파일이 있는지 확인
2. 데이터 파일에 실제 데이터가 있는지 확인 (빈 배열이 아닌지)
3. 필터 조건을 변경해보기 (예: 날짜 범위)

### 성능 문제

**증상**: 페이지 로딩이 느림

**해결 방법**:
1. 데이터 파일 크기 확인 (매우 큰 경우 샘플링 고려)
2. 브라우저 캐시 삭제
3. Streamlit 캐시 삭제: `streamlit cache clear`

## 개발

### 코드 스타일

프로젝트는 다음 컨벤션을 따릅니다:
- PEP 8 스타일 가이드
- Type hints 사용
- Docstrings (Google 스타일)

### 새로운 시각화 추가

1. `pages/` 디렉토리에 새 페이지 모듈 생성
2. `show_your_page()` 함수 구현
3. `main.py`에 페이지 라우팅 추가
4. 필요한 경우 `visualizations/` 또는 `processing/`에 헬퍼 함수 추가

### 테스트

```bash
# 테스트 실행 (구현 예정)
uv run pytest

# 특정 테스트 파일 실행
uv run pytest tests/test_data_loader.py
```

## 배포

### Streamlit Cloud

1. GitHub 저장소에 코드 푸시
2. [Streamlit Cloud](https://streamlit.io/cloud)에서 앱 배포
3. 데이터 파일을 저장소에 포함하거나 secrets로 관리

### Docker

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# uv 설치
RUN pip install uv

# 의존성 파일 복사
COPY pyproject.toml uv.lock ./

# 의존성 설치
RUN uv sync --frozen

# 애플리케이션 코드 복사
COPY . .

# 포트 노출
EXPOSE 8501

# 앱 실행
CMD ["uv", "run", "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
# Docker 이미지 빌드
docker build -t mongodb-viz .

# 컨테이너 실행
docker run -p 8501:8501 -v $(pwd)/data:/app/data mongodb-viz
```

## 라이선스

이 프로젝트는 내부 사용을 위한 것입니다.

## 기여

버그 리포트나 기능 제안은 이슈 트래커를 통해 제출해주세요.

## 지원

문제가 발생하면 다음을 확인하세요:
1. 이 README의 문제 해결 섹션
2. Streamlit 문서: https://docs.streamlit.io
3. Plotly 문서: https://plotly.com/python/

---

**Made with ❤️ using Streamlit and Plotly**
