"""
Data type definitions for FortyFive robot telemetry streaming.
Simple namespace classes for data types, MIME types, and file patterns.
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
    "safetensors",
    "json",
    "yaml",
    "toml",
    "msgpack",
    "vuer_msg",
    "zip",
    "tar",
]


class TimeSeries:
    """Time series data type definition."""

    type = "time_series"
    mimeType = "application/json"
    mimeTypes = ["application/json", "application/x-msgpack", "application/cbor"]
    patterns = ["*.timeseries"]
    description = "Time-indexed numerical data (telemetry, sensors, metrics)"
    storageBackend = "mongodb"


class Parameters:
    """Parameters data type definition."""

    type = "parameters"
    mimeType = "application/json"
    mimeTypes = ["application/json", "application/yaml", "application/toml"]
    patterns = ["*.params", "config.*", "params.*"]
    description = "Configuration parameters and hyperparameters"
    storageBackend = "mongodb"


class Images:
    """Images data type definition."""

    type = "images"
    mimeType = "image/jpeg"
    mimeTypes = ["image/jpeg", "image/png", "image/webp", "image/tiff", "image/bmp", "image/gif", "image/svg+xml", "image/x-raw"]


class Video:
    """Video data type definition."""

    type = "video"
    mimeType = "video/mp4"
    mimeTypes = ["video/mp4", "video/webm", "video/x-msvideo", "video/quicktime", "video/x-matroska", "video/H264", "video/H265"]


class Audio:
    """Audio data type definition."""

    type = "audio"
    mimeType = "audio/mpeg"
    mimeTypes = ["audio/mpeg", "audio/wav", "audio/ogg", "audio/webm", "audio/aac", "audio/flac", "audio/opus"]


class Log:
    """Log data type definition."""

    type = "log"
    mimeType = "text/plain"
    mimeTypes = ["text/plain", "application/x-ndjson", "text/x-log"]


class Markdown:
    """Markdown data type definition."""

    type = "markdown"
    mimeType = "text/markdown"
    mimeTypes = ["text/markdown", "text/x-markdown", "text/plain"]


class File:
    """Generic file data type definition."""

    type = "file"
    mimeType = "application/octet-stream"
    mimeTypes = ["application/octet-stream", "*/*"]


class Csv:
    """CSV data type definition."""

    type = "csv"
    mimeType = "text/csv"
    mimeTypes = ["text/csv", "application/csv", "text/tab-separated-values"]


class Safetensors:
    """Safetensors data type definition."""

    type = "safetensors"
    mimeType = "application/x-safetensors"
    mimeTypes = ["application/x-safetensors", "application/octet-stream"]


class Json:
    """JSON data type definition."""

    type = "json"
    mimeType = "application/json"
    mimeTypes = ["application/json", "text/json", "application/ld+json"]
    patterns = ["*.json", "*.jsonl", "*.ndjson"]
    serializable = True
    humanReadable = True


class Yaml:
    """YAML data type definition."""

    type = "yaml"
    mimeType = "application/yaml"
    mimeTypes = ["application/yaml", "text/yaml", "application/x-yaml"]
    patterns = ["*.yaml", "*.yml"]
    serializable = True
    humanReadable = True


class Toml:
    """TOML data type definition."""

    type = "toml"
    mimeType = "application/toml"
    mimeTypes = ["application/toml", "text/toml"]
    patterns = ["*.toml"]
    serializable = True
    humanReadable = True


class Msgpack:
    """MessagePack binary serialization format."""

    type = "msgpack"
    mimeType = "application/x-msgpack"
    mimeTypes = ["application/x-msgpack", "application/msgpack"]
    patterns = ["*.msgpack", "*.msgpk", "*.mp"]
    serializable = True
    humanReadable = False
    binaryFormat = True


class VuerMsg:
    """Vuer message format - MessagePack serialized with $dtype field.

    This is a MessagePack-encoded binary format where each message
    contains a special '$dtype' key that specifies the output type
    for proper deserialization and handling.
    """

    type = "vuer_msg"
    mimeType = "application/x-vuer-msg"
    mimeTypes = ["application/x-vuer-msg", "application/vuer"]
    patterns = ["*.vuer", "*.vuermsg", "*.vm"]
    serializable = True
    humanReadable = False
    binaryFormat = True
    serializationFormat = "msgpack"
    typeField = "$dtype"  # Special field that specifies the output type
    compressionBuiltIn = True


class Zip:
    """ZIP archive format for compressed file collections."""

    type = "zip"
    mimeType = "application/zip"
    mimeTypes = ["application/zip", "application/x-zip-compressed"]
    patterns = ["*.zip", "*.zipx"]
    isArchive = True
    supportsCompression = True
    supportsMultipleFiles = True
    binaryFormat = True


class Tar:
    """TAR archive format for file collections."""

    type = "tar"
    mimeType = "application/x-tar"
    mimeTypes = [
        "application/x-tar",
        "application/x-gtar",
        "application/x-gzip",  # for .tar.gz
        "application/x-bzip2",  # for .tar.bz2
        "application/x-xz",  # for .tar.xz
    ]
    patterns = ["*.tar", "*.tar.gz", "*.tgz", "*.tar.bz2", "*.tbz", "*.tar.xz", "*.txz"]
    isArchive = True
    supportsCompression = True  # When combined with gzip/bzip2/xz
    supportsMultipleFiles = True
    binaryFormat = True
