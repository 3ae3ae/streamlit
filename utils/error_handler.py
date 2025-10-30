"""
Error handling utilities for consistent error messages and logging.
"""

import logging
from functools import wraps
from typing import Callable

import streamlit as st

# Configure logging
logger = logging.getLogger(__name__)


def handle_page_errors(func: Callable) -> Callable:
    """
    Decorator to handle errors in page functions with user-friendly messages.
    
    This decorator wraps page functions to catch and display errors gracefully,
    ensuring users see helpful error messages instead of stack traces.
    
    Args:
        func: Page function to wrap
        
    Returns:
        Wrapped function with error handling
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            st.error("📁 데이터 파일을 찾을 수 없습니다")
            st.info("data 폴더에 필요한 JSON 파일이 있는지 확인해주세요.")
            logger.error(f"File not found in {func.__name__}: {e}")
        except PermissionError as e:
            st.error("🔒 데이터 파일에 접근할 수 없습니다")
            st.info("파일 권한을 확인해주세요.")
            logger.error(f"Permission error in {func.__name__}: {e}")
        except ValueError as e:
            st.error("⚠️ 데이터 형식 오류가 발생했습니다")
            st.info("데이터 파일의 형식이 올바른지 확인해주세요.")
            logger.error(f"Value error in {func.__name__}: {e}")
        except KeyError as e:
            st.error("🔑 필요한 데이터 필드를 찾을 수 없습니다")
            st.info(f"누락된 필드: {e}")
            logger.error(f"Key error in {func.__name__}: {e}")
        except Exception as e:
            st.error("❌ 예상치 못한 오류가 발생했습니다")
            st.info("페이지를 새로고침하거나 다른 페이지를 시도해보세요.")
            logger.error(f"Unexpected error in {func.__name__}: {e}", exc_info=True)
            
            # Show detailed error in expander for debugging
            with st.expander("🔍 상세 오류 정보 (개발자용)"):
                st.code(str(e))
    
    return wrapper


def show_data_loading_error(data_type: str, suggestion: str = None):
    """
    Display a consistent error message for data loading failures.
    
    Args:
        data_type: Type of data that failed to load (e.g., "사용자", "이슈")
        suggestion: Optional suggestion for the user
    """
    st.error(f"❌ {data_type} 데이터를 로드할 수 없습니다")
    
    if suggestion:
        st.info(f"💡 {suggestion}")
    else:
        st.info("데이터 파일이 data 폴더에 있는지 확인해주세요.")


def show_empty_data_warning(data_type: str, suggestion: str = None):
    """
    Display a consistent warning message for empty data.
    
    Args:
        data_type: Type of data that is empty (e.g., "사용자", "이슈")
        suggestion: Optional suggestion for the user
    """
    st.warning(f"⚠️ {data_type} 데이터가 없습니다")
    
    if suggestion:
        st.info(f"💡 {suggestion}")


def show_no_results_message(context: str):
    """
    Display a message when no results are found for a query.
    
    Args:
        context: Context of the search (e.g., "선택한 기간", "해당 사용자")
    """
    st.info(f"🔍 {context}에 대한 데이터를 찾을 수 없습니다")


def validate_dataframe(df, required_columns: list, data_type: str) -> bool:
    """
    Validate that a dataframe has required columns.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        data_type: Type of data for error messages
        
    Returns:
        True if valid, False otherwise
    """
    if df.empty:
        show_empty_data_warning(data_type)
        return False
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"❌ {data_type} 데이터에 필요한 필드가 없습니다")
        st.info(f"누락된 필드: {', '.join(missing_columns)}")
        logger.error(f"Missing columns in {data_type}: {missing_columns}")
        return False
    
    return True
