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
  s3://fortyfive-robot-data/{prefix-id}
  ├── raw/
  │   ├── camera/ego/
  │   │   ├── rgb/
  │   │   │   ├── {timestamp}.jpg
  │   │   │   └── meta.jsonl
  │   │   └── depth/
  │   │       ├── {timestamp}.png
  │   │       └── meta.jsonl
  │   ├── lidar/
  │   │   └── pointcloud/
  │   │       ├── {timestamp}.ply
  │   │       └── meta.jsonl
  │   └── logs/
  │       ├── system/
  │       │   ├── {log_id}.log
  │       │   └── meta.jsonl
  │       ├── telemetry/
  │       │   ├── {log_id}.jsonl
  │       │   └── meta.jsonl
  │       └── events/
  │           ├── {log_id}.jsonl
  │           └── meta.jsonl
  ├── compressed/
  │   ├── camera/ego/
  │   │   ├── rgb/
  │   │   │   ├── {lot_id}.mp4
  │   │   │   └── meta.jsonl
  │   │   └── depth/
  │   │       ├── {lot_id}.tar.gz
  │   │       └── meta.jsonl
  │   ├── lidar/
  │   │   └── pointcloud/
  │   │       ├── {lot_id}.tar.gz
  │   │       └── meta.jsonl
  │   ├── logs/
  │   │   ├── system/
  │   │   │   ├── {log_id}.tar.gz
  │   │   │   └── meta.jsonl
  │   │   ├── telemetry/
  │   │   │   ├── {log_id}.tar.gz
  │   │   │   └── meta.jsonl
  │   │   └── events/
  │   │       ├── {log_id}.tar.gz
  │   │       └── meta.jsonl
  │   └── bundles/
  │       └── {lot_id}_complete.tar.gz
  └── processed/
      └── {robot_id}/
          └── {session_id}/
              └── thumbnails/
  ```

### Data Compaction

Camera feeds are compacted using multiple strategies:

#### 1. Client side compression

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

Now you can view the real-time data in vuer.ai, or the
recorded data in the data-manager dashboard.

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

### Testing

```bash
# Unit tests
pytest client/tests/

# Integration test
./run_integration_test.sh
```

## License

Part of FortyFive ML Dashboard - All rights reserved.