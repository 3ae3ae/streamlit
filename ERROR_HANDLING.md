# Error Handling Documentation

## Overview

This document describes the error handling and user feedback improvements implemented in the MongoDB Visualization Tool.

## Error Handling Strategy

### 1. Layered Error Handling

The application implements error handling at multiple layers:

- **Data Loading Layer** (`data_loader.py`): Catches file I/O and parsing errors
- **Processing Layer** (`processing/aggregators.py`): Handles data transformation errors
- **Visualization Layer** (`visualizations/*.py`): Manages chart generation errors
- **Page Layer** (`pages/*.py`): Provides user-friendly error messages
- **Application Layer** (`main.py`): Catches fatal application errors

### 2. Error Types and Messages

#### File Not Found Errors
- **Icon**: 📁
- **Message**: "데이터 파일을 찾을 수 없습니다"
- **Suggestion**: Specific file path and location guidance

#### Permission Errors
- **Icon**: 🔒
- **Message**: "데이터 파일에 접근할 수 없습니다"
- **Suggestion**: Check file permissions

#### Data Format Errors
- **Icon**: ⚠️
- **Message**: "데이터 형식 오류가 발생했습니다"
- **Suggestion**: Verify data file format

#### Empty Data Warnings
- **Icon**: ⚠️
- **Message**: "데이터가 없습니다"
- **Context**: Specific data type that is empty

#### Unexpected Errors
- **Icon**: ❌
- **Message**: "예상치 못한 오류가 발생했습니다"
- **Suggestion**: Refresh page or try another page
- **Debug Info**: Expandable section with detailed error for developers

### 3. Loading Indicators

All data loading operations use Streamlit spinners with descriptive messages:

```python
with st.spinner("데이터를 로드하는 중..."):
    data = load_data()
```

Common loading messages:
- "사용자 데이터를 로드하는 중..."
- "정치 성향 히스토리 데이터를 로드하는 중..."
- "토픽 데이터를 로드하는 중..."
- "데이터를 집계하는 중..."
- "차트를 생성하는 중..."

### 4. Data Validation

Each page validates data before processing:

1. **Empty Check**: Verify dataframe is not empty
2. **Column Check**: Ensure required columns exist
3. **Type Check**: Validate data types where critical
4. **Range Check**: Verify date ranges and numeric values

### 5. Graceful Degradation

When errors occur:

1. **Log Error**: Record detailed error information for debugging
2. **Show User Message**: Display friendly, actionable error message
3. **Provide Context**: Explain what went wrong and how to fix it
4. **Continue Operation**: Don't crash the entire app
5. **Offer Alternatives**: Suggest other pages or actions

## Implementation Examples

### Data Loader Error Handling

```python
@st.cache_data
def load_users() -> pd.DataFrame:
    try:
        data = load_json_file("prod.users.json")
        
        if not data:
            logger.warning("No user data found in file")
            return pd.DataFrame()
        
        # Process data...
        return df
        
    except FileNotFoundError as e:
        logger.error(f"User data file not found: {e}")
        return pd.DataFrame()
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in user data file: {e}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error loading users: {e}", exc_info=True)
        return pd.DataFrame()
```

### Page Error Handling

```python
def show_page():
    try:
        # Load data with spinner
        with st.spinner("데이터를 로드하는 중..."):
            data = load_data()
        
        # Validate data
        if data.empty:
            st.warning("데이터가 없습니다.")
            return
        
        # Process and display...
        
    except FileNotFoundError as e:
        st.error("📁 데이터 파일을 찾을 수 없습니다")
        st.info("data 폴더에 파일이 있는지 확인해주세요.")
        logging.error(f"File not found: {e}")
    except Exception as e:
        st.error("❌ 예상치 못한 오류가 발생했습니다")
        st.info("페이지를 새로고침하거나 다른 페이지를 시도해보세요.")
        logging.error(f"Error: {e}", exc_info=True)
        
        with st.expander("🔍 상세 오류 정보 (개발자용)"):
            st.code(str(e))
```

## User Experience Improvements

### 1. Clear Error Messages
- Use emojis for visual clarity
- Provide specific, actionable information
- Avoid technical jargon in user-facing messages

### 2. Helpful Suggestions
- Guide users to fix common issues
- Suggest alternative actions
- Provide context about what went wrong

### 3. Developer Debug Info
- Detailed errors in expandable sections
- Full stack traces in logs
- Error context for troubleshooting

### 4. Loading Feedback
- Spinners for all async operations
- Descriptive loading messages
- Progress indication where applicable

### 5. Graceful Failures
- App continues running after errors
- Users can navigate to other pages
- No full application crashes

## Testing Error Handling

To test error handling:

1. **Missing Files**: Remove data files and verify error messages
2. **Corrupted Data**: Modify JSON files to be invalid
3. **Empty Data**: Use empty JSON arrays
4. **Permission Issues**: Change file permissions
5. **Invalid Input**: Enter non-existent IDs or invalid dates

## Logging

All errors are logged with appropriate levels:

- `logger.info()`: Normal operations
- `logger.warning()`: Recoverable issues
- `logger.error()`: Errors with context
- `exc_info=True`: Include stack trace for debugging

Logs help developers diagnose issues without exposing technical details to users.

## Future Improvements

Potential enhancements:

1. **Retry Logic**: Automatic retry for transient failures
2. **Error Analytics**: Track common errors for improvement
3. **User Feedback**: Allow users to report issues
4. **Health Checks**: Proactive data validation on startup
5. **Fallback Data**: Use sample data when real data unavailable
