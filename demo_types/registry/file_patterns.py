"""
File pattern matching and MIME type utilities.
"""

from typing import List, Optional
import fnmatch
from .data_types import DataType, DATA_TYPE_REGISTRY


def get_data_type_for_file(filename: str) -> DataType:
    """Determine data type based on file patterns."""
    filename_lower = filename.lower()
    
    for dtype_string, dtype_class in DATA_TYPE_REGISTRY.items():
        if dtype_string == "file":
            continue
        
        for pattern in dtype_class.patterns:
            if fnmatch.fnmatch(filename_lower, pattern.lower()):
                return dtype_string
    
    return "file"


def get_mime_type_for_file(filename: str) -> str:
    """Get primary MIME type based on file pattern."""
    dtype = get_data_type_for_file(filename)
    dtype_class = DATA_TYPE_REGISTRY.get(dtype)
    
    if dtype_class and hasattr(dtype_class, 'mime_types') and dtype_class.mime_types:
        return dtype_class.mime_types[0]
    
    return "application/octet-stream"


def get_mime_types_for_data_type(data_type: DataType) -> List[str]:
    """Get all MIME types for a data type."""
    dtype_class = DATA_TYPE_REGISTRY.get(data_type)
    if dtype_class and hasattr(dtype_class, 'mime_types'):
        return dtype_class.mime_types
    return ["application/octet-stream"]


def get_file_patterns_for_data_type(data_type: DataType) -> List[str]:
    """Get all file patterns for a data type."""
    dtype_class = DATA_TYPE_REGISTRY.get(data_type)
    if dtype_class and hasattr(dtype_class, 'patterns'):
        return dtype_class.patterns
    return []


def matches_pattern(filename: str, data_type: DataType) -> bool:
    """Check if filename matches any pattern for the data type."""
    dtype_class = DATA_TYPE_REGISTRY.get(data_type)
    if not dtype_class or not hasattr(dtype_class, 'patterns'):
        return False
    
    if "*" in dtype_class.patterns and len(dtype_class.patterns) == 1:
        return True
    
    filename_lower = filename.lower()
    for pattern in dtype_class.patterns:
        if fnmatch.fnmatch(filename_lower, pattern.lower()):
            return True
    
    return False