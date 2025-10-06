"""
Data type definitions for FortyFive robot telemetry streaming.
Simple namespace classes for data types and MIME types.
"""

from typing import Literal


# Data type literals
DataType = Literal[
    "time_series",
    "parameters", 
    "images",
    "video",
    "audio",
    "log",
    "markdown",
    "file",
    "csv",
    "safetensors"
]


class TimeSeriesType:
    """Time series data type definition."""
    type = "time_series"
    mime_types = ["application/json", "application/x-msgpack", "application/cbor"]
    patterns = ["*.json", "*.msgpack", "*.cbor", "*.timeseries"]
    description = "Time-indexed numerical data (telemetry, sensors, metrics)"
    storage_backend = "mongodb"
    compression_supported = True
    streaming_supported = True
    max_size_mb = 100


class ParametersType:
    """Parameters data type definition."""
    type = "parameters"
    mime_types = ["application/json", "application/yaml", "application/toml"]
    patterns = ["*.json", "*.yaml", "*.yml", "*.toml", "*.params", "config.*", "params.*"]
    description = "Configuration parameters and hyperparameters"
    storage_backend = "mongodb"


class ImagesType:
    """Images data type definition."""
    type = "images"
    mime_types = [
        "image/jpeg", "image/png", "image/webp", "image/tiff",
        "image/bmp", "image/gif", "image/svg+xml", "image/x-raw"
    ]
    patterns = ["*.{jpg,jpeg,png,webp,tiff,tif,bmp,gif,svg,raw,nef,cr2,arw}"]
    description = "Static images including RGB, depth, thermal, and raw sensor data"
    storage_backend = "s3"
    compression_supported = True
    streaming_supported = False
    max_size_mb = 50


class VideoType:
    """Video data type definition."""
    type = "video"
    mime_types = [
        "video/mp4", "video/webm", "video/x-msvideo", "video/quicktime",
        "video/x-matroska", "video/H264", "video/H265"
    ]
    patterns = ["*.{mp4,webm,avi,mov,mkv,h264,h265,hevc,m4v,wmv}"]
    description = "Video streams from cameras and recorded sessions"
    storage_backend = "s3"
    compression_supported = True
    streaming_supported = True
    max_size_mb = 5000


class AudioType:
    """Audio data type definition."""
    type = "audio"
    mime_types = [
        "audio/mpeg", "audio/wav", "audio/ogg", "audio/webm",
        "audio/aac", "audio/flac", "audio/opus"
    ]
    patterns = ["*.{mp3,wav,ogg,webm,aac,flac,opus,m4a,wma}"]
    description = "Audio recordings and streams from microphones"
    storage_backend = "s3"
    compression_supported = True
    streaming_supported = True
    max_size_mb = 500


class LogType:
    """Log data type definition."""
    type = "log"
    mime_types = ["text/plain", "application/x-ndjson", "text/x-log"]
    patterns = ["*.log", "*.log.*", "*.ndjson", "*.jsonl", "*.stdout", "*.stderr", "logs/*.txt"]
    description = "Text logs from system components and applications"
    storage_backend = "mongodb"
    compression_supported = True
    streaming_supported = True
    max_size_mb = 100


class MarkdownType:
    """Markdown data type definition."""
    type = "markdown"
    mime_types = ["text/markdown", "text/x-markdown", "text/plain"]
    patterns = ["*.md", "*.markdown", "*.mdown", "*.mkd", "README*", "CHANGELOG*"]
    description = "Documentation and formatted text notes"
    storage_backend = "mongodb"
    compression_supported = True
    streaming_supported = False
    max_size_mb = 10


class FileType:
    """Generic file data type definition."""
    type = "file"
    mime_types = ["application/octet-stream", "*/*"]
    patterns = ["*"]
    description = "Generic file storage for any binary or text data"
    storage_backend = "s3"
    compression_supported = True
    streaming_supported = False
    max_size_mb = 1000


class CsvType:
    """CSV data type definition."""
    type = "csv"
    mime_types = ["text/csv", "application/csv", "text/tab-separated-values"]
    patterns = ["*.{csv,tsv,tab}", "data/*.csv"]
    description = "Tabular data in comma or tab-separated format"
    storage_backend = "both"
    compression_supported = True
    streaming_supported = False
    max_size_mb = 500


class SafetensorsType:
    """Safetensors data type definition."""
    type = "safetensors"
    mime_types = ["application/x-safetensors", "application/octet-stream"]
    patterns = ["*.safetensors", "*.st", "model_*.st"]
    description = "Safe serialization format for ML model tensors"
    storage_backend = "s3"
    compression_supported = False
    streaming_supported = False
    max_size_mb = 10000


# Registry mapping type strings to classes
DATA_TYPE_REGISTRY = {
    "time_series": TimeSeriesType,
    "parameters": ParametersType,
    "images": ImagesType,
    "video": VideoType,
    "audio": AudioType,
    "log": LogType,
    "markdown": MarkdownType,
    "file": FileType,
    "csv": CsvType,
    "safetensors": SafetensorsType,
}