/**
 * Data type definitions for FortyFive robot telemetry streaming.
 * Includes MIME types, file patterns, and metadata for each data type.
 */

export enum DataTypeEnum {
  TIME_SERIES = 'time_series',
  PARAMETERS = 'parameters',
  IMAGES = 'images',
  VIDEO = 'video',
  AUDIO = 'audio',
  LOG = 'log',
  MARKDOWN = 'markdown',
  FILE = 'file',
  CSV = 'csv',
  SAFETENSORS = 'safetensors',
}

export interface DataTypeDefinition {
  type: DataTypeEnum;
  mimeTypes: string[];
  fileSuffixes: string[];
  description: string;
  storageBackend: 'mongodb' | 's3' | 'both';
  compressionSupported: boolean;
  streamingSupported: boolean;
  maxSizeMB?: number;
}

// Define all data type specifications
export const DATA_TYPE_DEFINITIONS: Record<DataTypeEnum, DataTypeDefinition> = {
  [DataTypeEnum.TIME_SERIES]: {
    type: DataTypeEnum.TIME_SERIES,
    mimeTypes: ['application/json', 'application/x-msgpack', 'application/cbor'],
    fileSuffixes: ['.json', '.msgpack', '.cbor', '.timeseries'],
    description: 'Time-indexed numerical data (telemetry, sensors, metrics)',
    storageBackend: 'mongodb',
    compressionSupported: true,
    streamingSupported: true,
    maxSizeMB: 100,
  },

  [DataTypeEnum.PARAMETERS]: {
    type: DataTypeEnum.PARAMETERS,
    mimeTypes: ['application/json', 'application/yaml', 'application/toml'],
    fileSuffixes: ['.json', '.yaml', '.yml', '.toml', '.params'],
    description: 'Configuration parameters and hyperparameters',
    storageBackend: 'mongodb',
    compressionSupported: false,
    streamingSupported: false,
    maxSizeMB: 10,
  },

  [DataTypeEnum.IMAGES]: {
    type: DataTypeEnum.IMAGES,
    mimeTypes: [
      'image/jpeg',
      'image/png',
      'image/webp',
      'image/tiff',
      'image/bmp',
      'image/gif',
      'image/svg+xml',
      'image/x-raw',
    ],
    fileSuffixes: [
      '.jpg',
      '.jpeg',
      '.png',
      '.webp',
      '.tiff',
      '.tif',
      '.bmp',
      '.gif',
      '.svg',
      '.raw',
      '.nef',
      '.cr2',
      '.arw',
    ],
    description: 'Static images including RGB, depth, thermal, and raw sensor data',
    storageBackend: 's3',
    compressionSupported: true,
    streamingSupported: false,
    maxSizeMB: 50,
  },

  [DataTypeEnum.VIDEO]: {
    type: DataTypeEnum.VIDEO,
    mimeTypes: [
      'video/mp4',
      'video/webm',
      'video/x-msvideo',
      'video/quicktime',
      'video/x-matroska',
      'video/H264',
      'video/H265',
    ],
    fileSuffixes: [
      '.mp4',
      '.webm',
      '.avi',
      '.mov',
      '.mkv',
      '.h264',
      '.h265',
      '.hevc',
      '.m4v',
      '.wmv',
    ],
    description: 'Video streams from cameras and recorded sessions',
    storageBackend: 's3',
    compressionSupported: true,
    streamingSupported: true,
    maxSizeMB: 5000,
  },

  [DataTypeEnum.AUDIO]: {
    type: DataTypeEnum.AUDIO,
    mimeTypes: [
      'audio/mpeg',
      'audio/wav',
      'audio/ogg',
      'audio/webm',
      'audio/aac',
      'audio/flac',
      'audio/opus',
    ],
    fileSuffixes: ['.mp3', '.wav', '.ogg', '.webm', '.aac', '.flac', '.opus', '.m4a', '.wma'],
    description: 'Audio recordings and streams from microphones',
    storageBackend: 's3',
    compressionSupported: true,
    streamingSupported: true,
    maxSizeMB: 500,
  },

  [DataTypeEnum.LOG]: {
    type: DataTypeEnum.LOG,
    mimeTypes: ['text/plain', 'application/x-ndjson', 'text/x-log'],
    fileSuffixes: ['.log', '.txt', '.ndjson', '.jsonl', '.stdout', '.stderr'],
    description: 'Text logs from system components and applications',
    storageBackend: 'mongodb',
    compressionSupported: true,
    streamingSupported: true,
    maxSizeMB: 100,
  },

  [DataTypeEnum.MARKDOWN]: {
    type: DataTypeEnum.MARKDOWN,
    mimeTypes: ['text/markdown', 'text/x-markdown', 'text/plain'],
    fileSuffixes: ['.md', '.markdown', '.mdown', '.mkd'],
    description: 'Documentation and formatted text notes',
    storageBackend: 'mongodb',
    compressionSupported: true,
    streamingSupported: false,
    maxSizeMB: 10,
  },

  [DataTypeEnum.FILE]: {
    type: DataTypeEnum.FILE,
    mimeTypes: ['application/octet-stream', '*/*'],
    fileSuffixes: ['*'], // Matches any file
    description: 'Generic file storage for any binary or text data',
    storageBackend: 's3',
    compressionSupported: true,
    streamingSupported: false,
    maxSizeMB: 1000,
  },

  [DataTypeEnum.CSV]: {
    type: DataTypeEnum.CSV,
    mimeTypes: ['text/csv', 'application/csv', 'text/tab-separated-values'],
    fileSuffixes: ['.csv', '.tsv', '.tab'],
    description: 'Tabular data in comma or tab-separated format',
    storageBackend: 'both',
    compressionSupported: true,
    streamingSupported: false,
    maxSizeMB: 500,
  },

  [DataTypeEnum.SAFETENSORS]: {
    type: DataTypeEnum.SAFETENSORS,
    mimeTypes: ['application/x-safetensors', 'application/octet-stream'],
    fileSuffixes: ['.safetensors', '.st'],
    description: 'Safe serialization format for ML model tensors',
    storageBackend: 's3',
    compressionSupported: false, // Already optimized format
    streamingSupported: false,
    maxSizeMB: 10000,
  },
};

// Base interface for all data payloads
export interface DataPayload {
  timestamp: number; // Unix timestamp with milliseconds
  robotId: string;
  sessionId: string;
  dataType: DataTypeEnum;
  sequenceNumber: number;
  metadata: Record<string, any>;

  // Type-specific fields
  data?: Uint8Array | string | Record<string, any> | any[];
  mimeType?: string;
  encoding?: 'base64' | 'gzip' | 'raw' | string;
  compression?: 'gzip' | 'lz4' | 'zstd' | string;
  originalSize?: number;
  compressedSize?: number;
  checksum?: string; // SHA256 or MD5

  // Storage references
  s3Key?: string;
  mongodbId?: string;
}

// Time-series specific payload
export interface TimeSeriesData extends DataPayload {
  dataType: DataTypeEnum.TIME_SERIES;

  // Time-series specific
  metrics: Record<string, number>;
  labels: Record<string, string>;
  sampleRateHz?: number;
  aggregationWindowMs?: number;

  // Telemetry data
  pose?: {
    position: { x: number; y: number; z: number };
    orientation: { x: number; y: number; z: number; w: number };
  };
  joints?: number[];
  sensors?: Record<string, number>;
}

// Image specific payload
export interface ImageData extends DataPayload {
  dataType: DataTypeEnum.IMAGES;

  // Image specific
  width: number;
  height: number;
  channels: number;
  bitDepth: number;
  colorSpace: 'RGB' | 'BGR' | 'GRAY' | 'DEPTH' | string;
  cameraId?: string;
  frameNumber?: number;
  exposureMs?: number;
  gainDb?: number;

  // Thumbnails
  thumbnailS3Key?: string;
  previewS3Key?: string;
}

// Video specific payload
export interface VideoData extends DataPayload {
  dataType: DataTypeEnum.VIDEO;

  // Video specific
  width: number;
  height: number;
  fps: number;
  durationSeconds?: number;
  codec?: 'H.264' | 'H.265' | 'VP9' | string;
  bitrateKbps?: number;
  keyframeInterval?: number;
  cameraId?: string;

  // Streaming
  isLive: boolean;
  segmentNumber?: number;
  segmentDurationMs?: number;
}

// Audio specific payload
export interface AudioData extends DataPayload {
  dataType: DataTypeEnum.AUDIO;

  // Audio specific
  sampleRate: number;
  channels: number;
  bitDepth: number;
  durationSeconds?: number;
  codec?: 'mp3' | 'aac' | 'opus' | 'flac' | string;
  bitrateKbps?: number;
  microphoneId?: string;
}

// Log specific payload
export interface LogData extends DataPayload {
  dataType: DataTypeEnum.LOG;

  // Log specific
  level: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL';
  loggerName?: string;
  message: string;
  sourceFile?: string;
  lineNumber?: number;
  functionName?: string;
  stackTrace?: string;
  context: Record<string, any>;
}

// Markdown specific payload
export interface MarkdownData extends DataPayload {
  dataType: DataTypeEnum.MARKDOWN;

  // Markdown specific
  title?: string;
  content: string;
  frontmatter?: Record<string, any>;
  tableOfContents?: string[];
}

// CSV specific payload
export interface CsvData extends DataPayload {
  dataType: DataTypeEnum.CSV;

  // CSV specific
  headers: string[];
  rowCount: number;
  delimiter: ',' | '\t' | ';' | '|';
  hasHeaders: boolean;
  encoding: 'utf-8' | 'utf-16' | 'ascii' | string;
}

// Safetensors specific payload
export interface SafetensorsData extends DataPayload {
  dataType: DataTypeEnum.SAFETENSORS;

  // Safetensors specific
  tensors: Record<string, {
    shape: number[];
    dtype: 'float32' | 'float16' | 'int32' | 'int64' | string;
    size: number;
  }>;
  metadata?: Record<string, string>;
  version: string;
}

// Generic file payload
export interface FileData extends DataPayload {
  dataType: DataTypeEnum.FILE;

  // File specific
  filename: string;
  fileExtension: string;
  detectedMimeType?: string;
}

// Type guard functions
export function isTimeSeriesData(payload: DataPayload): payload is TimeSeriesData {
  return payload.dataType === DataTypeEnum.TIME_SERIES;
}

export function isImageData(payload: DataPayload): payload is ImageData {
  return payload.dataType === DataTypeEnum.IMAGES;
}

export function isVideoData(payload: DataPayload): payload is VideoData {
  return payload.dataType === DataTypeEnum.VIDEO;
}

export function isAudioData(payload: DataPayload): payload is AudioData {
  return payload.dataType === DataTypeEnum.AUDIO;
}

export function isLogData(payload: DataPayload): payload is LogData {
  return payload.dataType === DataTypeEnum.LOG;
}

export function isMarkdownData(payload: DataPayload): payload is MarkdownData {
  return payload.dataType === DataTypeEnum.MARKDOWN;
}

export function isCsvData(payload: DataPayload): payload is CsvData {
  return payload.dataType === DataTypeEnum.CSV;
}

export function isSafetensorsData(payload: DataPayload): payload is SafetensorsData {
  return payload.dataType === DataTypeEnum.SAFETENSORS;
}

export function isFileData(payload: DataPayload): payload is FileData {
  return payload.dataType === DataTypeEnum.FILE;
}

// Utility functions
export function getDataTypeForFile(filename: string): DataTypeEnum {
  // Check specific types first (in order of specificity)
  for (const [dtype, definition] of Object.entries(DATA_TYPE_DEFINITIONS)) {
    if (dtype === DataTypeEnum.FILE) continue; // Skip generic file type

    const matches = definition.fileSuffixes.some((suffix) =>
      filename.toLowerCase().endsWith(suffix),
    );
    if (matches) {
      return dtype as DataTypeEnum;
    }
  }

  // Default to generic file type
  return DataTypeEnum.FILE;
}

export function getMimeTypeForFile(filename: string): string {
  const dtype = getDataTypeForFile(filename);
  const definition = DATA_TYPE_DEFINITIONS[dtype];
  return definition.mimeTypes[0] || 'application/octet-stream';
}

export function getPrimaryMimeType(dataType: DataTypeEnum): string {
  const definition = DATA_TYPE_DEFINITIONS[dataType];
  return definition.mimeTypes[0] || 'application/octet-stream';
}

export function validatePayloadSize(payload: DataPayload): boolean {
  const definition = DATA_TYPE_DEFINITIONS[payload.dataType];
  if (!definition.maxSizeMB) return true;

  const sizeMB = (payload.originalSize || 0) / (1024 * 1024);
  return sizeMB <= definition.maxSizeMB;
}

export function matchesSuffix(filename: string, dataType: DataTypeEnum): boolean {
  const definition = DATA_TYPE_DEFINITIONS[dataType];
  if (definition.fileSuffixes.includes('*')) return true;

  return definition.fileSuffixes.some((suffix) =>
    filename.toLowerCase().endsWith(suffix),
  );
}

// Export type for all specific data types
export type SpecificDataPayload =
  | TimeSeriesData
  | ImageData
  | VideoData
  | AudioData
  | LogData
  | MarkdownData
  | CsvData
  | SafetensorsData
  | FileData;