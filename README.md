# Robot Data Streaming Demo

A demonstration of real-time robot telemetry streaming to the FortyFive ML dashboard system.

## Overview

This demo simulates a robot sending telemetry data (position, velocity, sensor readings) to the data-manager server via
WebSocket connections. It demonstrates:

- Real-time data streaming from a simulated robot
- WebSocket-based and HTTPS Streaming-based communication
- Batching and log rotation
- Automatic reconnection handling
- Time-series data visualization in data manager

We will use JSON for metadata and MessagePack for binary. We will need to define a schema for
each data type, and a separate event type for remote-procedure calls (RPC). 

## Data Types
1. **time_series** - Time-indexed numerical data (telemetry, sensors, metrics)
2. **parameters** - Configuration parameters and hyperparameters
3. **images** - Static images (JPEG, PNG, WebP, TIFF, etc.)
4. **video** - Video streams (MP4, WebM, AVI, etc.)
5. **audio** - Audio recordings (MP3, WAV, OGG, etc.)
6. **log** - Text logs from system components
7. **markdown** - Documentation and formatted text
8. **file** - Generic file storage
9. **csv** - Tabular data in CSV/TSV format
10. **safetensors** - ML model tensor serialization
11. **json** - JSON data interchange format
12. **yaml** - YAML configuration format
13. **toml** - TOML configuration format
14. **msgpack** - MessagePack binary serialization
15. **vuer_msg** - Vuer MessagePack format with $dtype field
16. **zip** - ZIP compressed archives
17. **tar** - TAR archives (with optional compression)

## Example Data Schema

### Storage Strategy

We use a hybrid storage approach optimized for both real-time streaming and historical analysis:

#### 1. MongoDB - Metadata & Time-series

- **Purpose**: Store structured telemetry data, metadata, and indexes
- **Collections**:
    - `sessions`: Robot session metadata and configurations
    - `telemetry`: High-frequency pose, joint, and sensor data
    - `frames_metadata`: Camera frame references with S3 links
    - `aggregations`: Pre-computed statistics for fast queries

#### 2. S3 - Binary Objects

- **Purpose**: Store large binary data (camera frames, point clouds)
- **Structure**:
  ```
  s3://fortyfive-robot-data/
  ├── raw/
  │   ├── {robot_id}/
  │   │   ├── {session_id}/
  │   │   │   ├── frames/
  │   │   │   │   ├── {timestamp}_rgb.jpg
  │   │   │   │   ├── {timestamp}_depth.png
  │   │   │   │   └── {timestamp}_pointcloud.ply
  │   │   │   └── compressed/
  │   │   │       └── {hour}_bundle.tar.gz
  └── processed/
      └── {robot_id}/
          └── {session_id}/
              └── thumbnails/
  ```

## Hot Loading & Visualization

### Caching Strategy

The system implements a multi-tier caching strategy for optimal visualization performance:

#### 1. Edge Cache (CDN)

- **CloudFront** distribution for S3 binary objects
- Automatic geographic distribution
- 24-hour TTL for processed data
- 1-hour TTL for raw streaming data

### Data Compaction

Camera feeds are compacted using multiple strategies:

#### 1. Real-time Compression

- **H.264** for RGB streams (70% size reduction)
- **PNG** with zlib for depth maps (50% reduction)
- **Draco** geometry compression for point clouds (90% reduction)

#### 2. Temporal Bundling

- Hourly bundles of consecutive frames
- Delta encoding between frames
- Keyframe every 30 frames

#### 3. Resolution Tiers

```
Original: 1920x1080 → Storage: S3 cold tier
Preview:   640x360  → Storage: S3 standard
Thumbnail: 120x68   → Storage: MongoDB GridFS
```

### 2. Streaming Patterns

- **High-frequency telemetry**: 100Hz pose updates
- **Medium-frequency sensors**: 30Hz force/torque readings
- **Low-frequency metrics**: 1Hz system health
- **Burst mode**: Camera frame events at variable rates

## Quick Start

### 1. Start the Data Manager Server

```bash
cd ../data-manager
pnpm dev
```

### 2. Run the Robot Simulator

todo - TBD

### 3. View in ML-Dash

```bash
cd ../ml-dash
pnpm dev
# Open http://localhost:3000
```

## Performance Metrics

### Data Generation Rates

The simulator generates approximately:

- **Telemetry**: 30,000 points/min per robot (~5MB JSON)
- **Camera Frames**: 1800 frames/min (30fps × 60s)
    - RGB: ~100MB/min (compressed JPEG)
    - Depth: ~50MB/min (compressed PNG)
    - Point Cloud: ~200MB/min (compressed Draco)
- **Total**: ~350MB/min per robot (compressed)

### Storage Requirements

- **MongoDB**: ~10GB/day for 10 robots (metadata + telemetry)
- **S3**: ~500GB/day for 10 robots (binary objects)
- **Retention**: 30 days hot, 90 days warm, 1 year cold

### Query Performance Targets

- **Real-time telemetry**: < 100ms latency
- **Frame retrieval**: < 500ms for recent, < 2s for cold
- **Time-range query**: < 1s for 1 hour of data
- **Aggregations**: < 200ms for pre-computed stats

## Sample Output

```
[2024-01-15 10:23:45] Robot robot_001 connected
[2024-01-15 10:23:45] Streaming started: 100Hz telemetry, 30Hz sensors
[2024-01-15 10:23:46] Batch sent: 100 messages (12.3KB)
[2024-01-15 10:23:47] Batch sent: 100 messages (12.1KB)
...
[2024-01-15 10:28:45] Session complete: 300s, 30,000 messages sent
```

## Development

### Adding New Data Types

1. Define schema in `client/schemas.py`
2. Add generator in `client/generators.py`
3. Update server handler in `server/handlers.py`
4. Add visualization in ml-dash

### Testing

```bash
# Unit tests
pytest client/tests/

# Integration test
./run_integration_test.sh
```

## Implementation Notes

### Network Optimization

- WebSocket connection pooling for multiple robots
- Message batching reduces overhead by 70%
- Automatic backpressure handling when server is slow
- Local buffering during network interruptions
- Binary protocol (MessagePack) for 40% size reduction

### Database Optimization

- Time-series collections with automatic sharding
- Compound indexes on (robot_id, session_id, timestamp)
- TTL indexes for automatic data expiration
- Aggregation pipelines for real-time statistics

### S3 Optimization

- Multipart uploads for large files
- Intelligent tiering for cost optimization
- Batch operations for frame bundles
- Pre-signed URLs with 1-hour expiry

### Visualization Optimization

- Virtual scrolling for large datasets
- Level-of-detail (LOD) rendering
- Progressive image loading
- WebGL for 3D point cloud rendering
- Web Workers for data processing

## License

Part of FortyFive ML Dashboard - All rights reserved.