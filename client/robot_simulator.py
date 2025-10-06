#!/usr/bin/env python3
"""
Robot telemetry simulator for demonstrating real-time data streaming.
"""

import asyncio
import json
import time
import argparse
import random
import numpy as np
from datetime import datetime
from typing import Dict, Any, List
import websocket
import threading
from queue import Queue
import signal
import sys

class RobotSimulator:
    def __init__(self, robot_id: str, server_url: str = "ws://localhost:8080/ws"):
        self.robot_id = robot_id
        self.server_url = server_url
        self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.message_queue = Queue()
        self.running = False
        self.ws = None
        self.stats = {
            "messages_sent": 0,
            "bytes_sent": 0,
            "start_time": time.time()
        }
        
        # Robot state
        self.pose = {"x": 0.0, "y": 0.0, "z": 0.0, "qw": 1.0, "qx": 0.0, "qy": 0.0, "qz": 0.0}
        self.joint_positions = [0.0] * 7  # 7-DOF arm
        self.joint_velocities = [0.0] * 7
        
    def connect(self):
        """Establish WebSocket connection."""
        try:
            self.ws = websocket.WebSocketApp(
                self.server_url,
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            wst = threading.Thread(target=self.ws.run_forever)
            wst.daemon = True
            wst.start()
            return True
        except Exception as e:
            print(f"[{self.robot_id}] Connection failed: {e}")
            return False
    
    def on_open(self, ws):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Robot {self.robot_id} connected")
        self.running = True
        
    def on_message(self, ws, message):
        pass  # Handle server responses if needed
        
    def on_error(self, ws, error):
        print(f"[{self.robot_id}] WebSocket error: {error}")
        
    def on_close(self, ws, close_status_code, close_msg):
        print(f"[{self.robot_id}] Disconnected")
        self.running = False
    
    def generate_telemetry(self) -> Dict[str, Any]:
        """Generate telemetry data with realistic robot motion."""
        timestamp = time.time()
        
        # Simulate smooth robot motion
        self.pose["x"] += random.gauss(0.001, 0.0005)
        self.pose["y"] += random.gauss(0.001, 0.0005)
        self.pose["z"] = 0.5 + 0.1 * np.sin(timestamp * 0.5)
        
        # Update joint positions (sinusoidal motion)
        for i in range(7):
            self.joint_positions[i] = np.sin(timestamp * (0.5 + i * 0.1)) * (np.pi / 4)
            self.joint_velocities[i] = np.cos(timestamp * (0.5 + i * 0.1)) * (np.pi / 4) * (0.5 + i * 0.1)
        
        return {
            "timestamp": timestamp,
            "robot_id": self.robot_id,
            "session_id": self.session_id,
            "data_type": "telemetry",
            "payload": {
                "pose": self.pose.copy(),
                "joints": {
                    "positions": self.joint_positions.copy(),
                    "velocities": self.joint_velocities.copy(),
                    "torques": [random.gauss(0, 0.5) for _ in range(7)]
                }
            }
        }
    
    def generate_sensor_data(self) -> Dict[str, Any]:
        """Generate sensor readings."""
        timestamp = time.time()
        
        return {
            "timestamp": timestamp,
            "robot_id": self.robot_id,
            "session_id": self.session_id,
            "data_type": "sensors",
            "payload": {
                "force_torque": {
                    "force": [random.gauss(0, 1) for _ in range(3)],
                    "torque": [random.gauss(0, 0.1) for _ in range(3)]
                },
                "imu": {
                    "acceleration": [random.gauss(0, 0.1) for _ in range(3)],
                    "gyroscope": [random.gauss(0, 0.01) for _ in range(3)]
                },
                "temperature": 25.0 + random.gauss(0, 2)
            }
        }
    
    def generate_system_metrics(self) -> Dict[str, Any]:
        """Generate system health metrics."""
        timestamp = time.time()
        uptime = timestamp - self.stats["start_time"]
        
        return {
            "timestamp": timestamp,
            "robot_id": self.robot_id,
            "session_id": self.session_id,
            "data_type": "system",
            "payload": {
                "cpu_percent": 20 + random.gauss(10, 5),
                "memory_mb": 512 + random.gauss(50, 10),
                "network_latency_ms": 5 + random.gauss(2, 1),
                "uptime_seconds": uptime,
                "messages_sent": self.stats["messages_sent"]
            }
        }
    
    def send_batch(self, messages: List[Dict[str, Any]]):
        """Send a batch of messages."""
        if not self.ws or not self.running:
            return
            
        batch = {
            "batch_id": f"{self.robot_id}_{int(time.time() * 1000)}",
            "messages": messages
        }
        
        try:
            data = json.dumps(batch)
            self.ws.send(data)
            self.stats["messages_sent"] += len(messages)
            self.stats["bytes_sent"] += len(data)
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Batch sent: {len(messages)} messages ({len(data)/1024:.1f}KB)")
        except Exception as e:
            print(f"[{self.robot_id}] Failed to send batch: {e}")
    
    async def run_telemetry_loop(self, rate_hz: int = 100):
        """Generate telemetry at specified rate."""
        interval = 1.0 / rate_hz
        batch = []
        batch_size = 100
        
        while self.running:
            message = self.generate_telemetry()
            batch.append(message)
            
            if len(batch) >= batch_size:
                self.send_batch(batch)
                batch = []
            
            await asyncio.sleep(interval)
    
    async def run_sensor_loop(self, rate_hz: int = 30):
        """Generate sensor data at specified rate."""
        interval = 1.0 / rate_hz
        
        while self.running:
            message = self.generate_sensor_data()
            self.send_batch([message])
            await asyncio.sleep(interval)
    
    async def run_metrics_loop(self, rate_hz: int = 1):
        """Generate system metrics at specified rate."""
        interval = 1.0 / rate_hz
        
        while self.running:
            message = self.generate_system_metrics()
            self.send_batch([message])
            await asyncio.sleep(interval)
    
    async def run(self, duration: int = 300):
        """Run all data generation loops."""
        if not self.connect():
            return
        
        # Wait for connection
        await asyncio.sleep(1)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Streaming started: 100Hz telemetry, 30Hz sensors")
        
        try:
            # Run all loops concurrently
            await asyncio.wait_for(
                asyncio.gather(
                    self.run_telemetry_loop(100),
                    self.run_sensor_loop(30),
                    self.run_metrics_loop(1)
                ),
                timeout=duration
            )
        except asyncio.TimeoutError:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Session complete: {duration}s, {self.stats['messages_sent']} messages sent")
        finally:
            self.running = False
            if self.ws:
                self.ws.close()

async def main():
    parser = argparse.ArgumentParser(description="Robot telemetry simulator")
    parser.add_argument("--robots", type=int, default=1, help="Number of robots to simulate")
    parser.add_argument("--duration", type=int, default=300, help="Duration in seconds")
    parser.add_argument("--server", default="ws://localhost:8080/ws", help="WebSocket server URL")
    
    args = parser.parse_args()
    
    print(f"Starting {args.robots} robot simulator(s) for {args.duration} seconds")
    print(f"Server: {args.server}")
    print("-" * 50)
    
    # Create and run robot simulators
    robots = [RobotSimulator(f"robot_{i:03d}", args.server) for i in range(args.robots)]
    
    await asyncio.gather(*[robot.run(args.duration) for robot in robots])
    
    # Print statistics
    print("-" * 50)
    print("Session Statistics:")
    for robot in robots:
        print(f"  {robot.robot_id}: {robot.stats['messages_sent']} messages, {robot.stats['bytes_sent']/1024/1024:.2f} MB")

def signal_handler(sig, frame):
    print("\nShutting down...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    asyncio.run(main())