"""
Type definitions using Protocol and TypedDict for FortyFive streaming system.
These provide strict typing for data structures while maintaining flexibility.
"""

from typing import Protocol, TypedDict, List, Optional, Union, Any, Literal, runtime_checkable
from typing_extensions import NotRequired


class MimeTypeInfo(TypedDict):
    """MIME type information for each data type."""
    primary: str
    alternatives: List[str]
    description: str


# Data type MIME mappings
DATA_TYPE_MIMES: dict[str, MimeTypeInfo] = {
    "time_series": {
        "primary": "application/json",
        "alternatives": ["application/x-msgpack", "application/cbor"],
        "description": "Time-indexed numerical data"
    },
    "parameters": {
        "primary": "application/json",
        "alternatives": ["application/yaml", "application/toml"],
        "description": "Configuration parameters"
    },
    "images": {
        "primary": "image/jpeg",
        "alternatives": [
            "image/png", "image/webp", "image/tiff", "image/bmp",
            "image/gif", "image/svg+xml", "image/x-raw"
        ],
        "description": "Static images"
    },
    "video": {
        "primary": "video/mp4",
        "alternatives": [
            "video/webm", "video/x-msvideo", "video/quicktime",
            "video/x-matroska", "video/H264", "video/H265"
        ],
        "description": "Video streams"
    },
    "audio": {
        "primary": "audio/mpeg",
        "alternatives": [
            "audio/wav", "audio/ogg", "audio/webm",
            "audio/aac", "audio/flac", "audio/opus"
        ],
        "description": "Audio recordings"
    },
    "log": {
        "primary": "text/plain",
        "alternatives": ["application/x-ndjson", "text/x-log"],
        "description": "Text logs"
    },
    "markdown": {
        "primary": "text/markdown",
        "alternatives": ["text/x-markdown", "text/plain"],
        "description": "Markdown documentation"
    },
    "file": {
        "primary": "application/octet-stream",
        "alternatives": ["*/*"],
        "description": "Generic file"
    },
    "csv": {
        "primary": "text/csv",
        "alternatives": ["application/csv", "text/tab-separated-values"],
        "description": "Tabular data"
    },
    "safetensors": {
        "primary": "application/x-safetensors",
        "alternatives": ["application/octet-stream"],
        "description": "ML model tensors"
    }
}


class FilePatternInfo(TypedDict):
    """File pattern information for each data type."""
    extensions: List[str]
    patterns: List[str]  # glob patterns
    case_sensitive: bool


# File suffix patterns
FILE_PATTERNS: dict[str, FilePatternInfo] = {
    "time_series": {
        "extensions": [".json", ".msgpack", ".cbor", ".timeseries"],
        "patterns": ["*.timeseries", "*_telemetry.json"],
        "case_sensitive": False
    },
    "parameters": {
        "extensions": [".json", ".yaml", ".yml", ".toml", ".params"],
        "patterns": ["config.*", "params.*", "*.config.json"],
        "case_sensitive": False
    },
    "images": {
        "extensions": [
            ".jpg", ".jpeg", ".png", ".webp", ".tiff", ".tif",
            ".bmp", ".gif", ".svg", ".raw", ".nef", ".cr2", ".arw"
        ],
        "patterns": ["*.{jpg,jpeg,png}", "*_frame_*.jpg"],
        "case_sensitive": False
    },
    "video": {
        "extensions": [
            ".mp4", ".webm", ".avi", ".mov", ".mkv",
            ".h264", ".h265", ".hevc", ".m4v", ".wmv"
        ],
        "patterns": ["*.{mp4,webm,mkv}", "*_recording_*.mp4"],
        "case_sensitive": False
    },
    "audio": {
        "extensions": [
            ".mp3", ".wav", ".ogg", ".webm", ".aac",
            ".flac", ".opus", ".m4a", ".wma"
        ],
        "patterns": ["*.{mp3,wav,ogg}", "audio_*.wav"],
        "case_sensitive": False
    },
    "log": {
        "extensions": [".log", ".txt", ".ndjson", ".jsonl", ".stdout", ".stderr"],
        "patterns": ["*.log", "*.log.*", "logs/*.txt"],
        "case_sensitive": False
    },
    "markdown": {
        "extensions": [".md", ".markdown", ".mdown", ".mkd"],
        "patterns": ["*.md", "README*", "CHANGELOG*"],
        "case_sensitive": False
    },
    "csv": {
        "extensions": [".csv", ".tsv", ".tab"],
        "patterns": ["*.{csv,tsv}", "data/*.csv"],
        "case_sensitive": False
    },
    "safetensors": {
        "extensions": [".safetensors", ".st"],
        "patterns": ["*.safetensors", "model_*.st"],
        "case_sensitive": False
    },
    "file": {
        "extensions": ["*"],
        "patterns": ["*"],
        "case_sensitive": False
    }
}


# TypedDict definitions for structured data
class Position3D(TypedDict):
    """3D position coordinates."""
    x: float
    y: float
    z: float


class Quaternion(TypedDict):
    """Quaternion for orientation."""
    x: float
    y: float
    z: float
    w: float


class Pose(TypedDict):
    """Robot pose data."""
    position: Position3D
    orientation: Quaternion


class BasePayload(TypedDict):
    """Base payload structure for all data types."""
    timestamp: float
    robot_id: str
    session_id: str
    data_type: Literal[
        "time_series", "parameters", "images", "video", "audio",
        "log", "markdown", "file", "csv", "safetensors"
    ]
    sequence_number: int
    metadata: dict[str, Any]
    mime_type: NotRequired[str]
    encoding: NotRequired[Literal["base64", "gzip", "raw"]]
    compression: NotRequired[Literal["gzip", "lz4", "zstd"]]
    original_size: NotRequired[int]
    compressed_size: NotRequired[int]
    checksum: NotRequired[str]
    s3_key: NotRequired[str]
    mongodb_id: NotRequired[str]


class TimeSeriesPayload(BasePayload):
    """Time-series specific payload."""
    data_type: Literal["time_series"]
    metrics: dict[str, float]
    labels: dict[str, str]
    sample_rate_hz: NotRequired[float]
    aggregation_window_ms: NotRequired[int]
    pose: NotRequired[Pose]
    joints: NotRequired[List[float]]
    sensors: NotRequired[dict[str, float]]


class ImagePayload(BasePayload):
    """Image specific payload."""
    data_type: Literal["images"]
    width: int
    height: int
    channels: int
    bit_depth: int
    color_space: Literal["RGB", "BGR", "GRAY", "DEPTH"]
    camera_id: NotRequired[str]
    frame_number: NotRequired[int]
    exposure_ms: NotRequired[float]
    gain_db: NotRequired[float]
    thumbnail_s3_key: NotRequired[str]
    preview_s3_key: NotRequired[str]


class VideoPayload(BasePayload):
    """Video specific payload."""
    data_type: Literal["video"]
    width: int
    height: int
    fps: float
    duration_seconds: NotRequired[float]
    codec: NotRequired[Literal["H.264", "H.265", "VP9"]]
    bitrate_kbps: NotRequired[int]
    keyframe_interval: NotRequired[int]
    camera_id: NotRequired[str]
    is_live: bool
    segment_number: NotRequired[int]
    segment_duration_ms: NotRequired[int]


class AudioPayload(BasePayload):
    """Audio specific payload."""
    data_type: Literal["audio"]
    sample_rate: int
    channels: int
    bit_depth: int
    duration_seconds: NotRequired[float]
    codec: NotRequired[Literal["mp3", "aac", "opus", "flac"]]
    bitrate_kbps: NotRequired[int]
    microphone_id: NotRequired[str]


class LogPayload(BasePayload):
    """Log specific payload."""
    data_type: Literal["log"]
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    logger_name: NotRequired[str]
    message: str
    source_file: NotRequired[str]
    line_number: NotRequired[int]
    function_name: NotRequired[str]
    stack_trace: NotRequired[str]
    context: dict[str, Any]


class MarkdownPayload(BasePayload):
    """Markdown specific payload."""
    data_type: Literal["markdown"]
    title: NotRequired[str]
    content: str
    frontmatter: NotRequired[dict[str, Any]]
    table_of_contents: NotRequired[List[str]]


class CsvPayload(BasePayload):
    """CSV specific payload."""
    data_type: Literal["csv"]
    headers: List[str]
    row_count: int
    delimiter: Literal[",", "\t", ";", "|"]
    has_headers: bool
    encoding: str


class TensorInfo(TypedDict):
    """Information about a tensor."""
    shape: List[int]
    dtype: Literal["float32", "float16", "int32", "int64"]
    size: int


class SafetensorsPayload(BasePayload):
    """Safetensors specific payload."""
    data_type: Literal["safetensors"]
    tensors: dict[str, TensorInfo]
    metadata: NotRequired[dict[str, str]]
    version: str


class FilePayload(BasePayload):
    """Generic file payload."""
    data_type: Literal["file"]
    filename: str
    file_extension: str
    detected_mime_type: NotRequired[str]


# Union type for all payload types
Payload = Union[
    TimeSeriesPayload,
    ImagePayload,
    VideoPayload,
    AudioPayload,
    LogPayload,
    MarkdownPayload,
    CsvPayload,
    SafetensorsPayload,
    FilePayload
]


# Protocol definitions for runtime checking
@runtime_checkable
class DataProcessor(Protocol):
    """Protocol for data processors."""
    
    def process(self, payload: Payload) -> bytes:
        """Process a payload into bytes for storage."""
        ...
    
    def validate(self, payload: Payload) -> bool:
        """Validate a payload structure."""
        ...
    
    def get_mime_type(self) -> str:
        """Get the MIME type this processor handles."""
        ...


@runtime_checkable
class StorageBackend(Protocol):
    """Protocol for storage backends."""
    
    async def store(self, key: str, data: bytes, metadata: dict[str, Any]) -> str:
        """Store data and return storage key."""
        ...
    
    async def retrieve(self, key: str) -> bytes:
        """Retrieve data by key."""
        ...
    
    async def delete(self, key: str) -> bool:
        """Delete data by key."""
        ...
    
    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        ...


@runtime_checkable
class Compressor(Protocol):
    """Protocol for data compression."""
    
    def compress(self, data: bytes) -> bytes:
        """Compress data."""
        ...
    
    def decompress(self, data: bytes) -> bytes:
        """Decompress data."""
        ...
    
    def get_compression_ratio(self, original: bytes, compressed: bytes) -> float:
        """Calculate compression ratio."""
        ...


# Helper function to get MIME type
def get_mime_type(data_type: str) -> str:
    """Get primary MIME type for a data type."""
    return DATA_TYPE_MIMES.get(data_type, {}).get("primary", "application/octet-stream")


# Helper function to get all MIME types
def get_all_mime_types(data_type: str) -> List[str]:
    """Get all MIME types for a data type."""
    info = DATA_TYPE_MIMES.get(data_type, {})
    if not info:
        return ["application/octet-stream"]
    return [info["primary"]] + info.get("alternatives", [])


# Helper function to get file extensions
def get_file_extensions(data_type: str) -> List[str]:
    """Get file extensions for a data type."""
    return FILE_PATTERNS.get(data_type, {}).get("extensions", [])


# Helper function to match file to data type
def match_file_type(filename: str) -> Optional[str]:
    """Match a filename to a data type based on extension."""
    filename_lower = filename.lower()
    
    for data_type, pattern_info in FILE_PATTERNS.items():
        if data_type == "file":  # Skip generic file type
            continue
            
        for ext in pattern_info["extensions"]:
            if ext == "*":
                continue
            if filename_lower.endswith(ext):
                return data_type
    
    return "file"  # Default to generic file type