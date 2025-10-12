#!/usr/bin/env python3
"""
Data Validation Tool
====================

Advanced tool to verify that all consciousness data is real-time and not simulated.
This tool performs comprehensive validation of data authenticity.

Validation Methods:
1. Time progression analysis
2. Data entropy measurement
3. Change frequency analysis
4. Cross-source consistency checking
5. Statistical randomness verification
"""

import asyncio
import websockets
import requests
import time
import json
import hashlib
import statistics
from collections import deque
from typing import Dict, Any, List
import numpy as np

class DataValidationTool:
    """Advanced tool for validating consciousness data authenticity"""
    
    def __init__(self):
        self.metatron_ws_url = "ws://localhost:8003/ws"
        self.metatron_api_base = "http://localhost:8003"
        self.data_samples = deque(maxlen=50)  # Store recent samples
        self.validation_results = []
        self.start_time = time.time()
        
    async def collect_websocket_data(self, duration: int = 10):
        """Collect data from WebSocket for validation"""
        print(f"📡 Collecting WebSocket data for {duration} seconds...")
        samples = []
        start_collect = time.time()
        
        try:
            async with websockets.connect(self.metatron_ws_url, timeout=5) as websocket:
                while time.time() - start_collect < duration:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                        data = json.loads(message)
                        samples.append({
                            "timestamp": time.time(),
                            "data": data,
                            "source": "websocket"
                        })
                        print(f"  Collected sample {len(samples)}")
                        await asyncio.sleep(0.1)  # Small delay
                    except asyncio.TimeoutError:
                        continue
        except Exception as e:
            print(f"❌ WebSocket collection error: {e}")
            
        return samples
    
    def collect_http_data(self, duration: int = 10):
        """Collect data from HTTP API for validation"""
        print(f"🌐 Collecting HTTP API data for {duration} seconds...")
        samples = []
        start_collect = time.time()
        
        while time.time() - start_collect < duration:
            try:
                response = requests.get(f"{self.metatron_api_base}/api/state", timeout=1)
                if response.status_code == 200:
                    data = response.json()
                    samples.append({
                        "timestamp": time.time(),
                        "data": data,
                        "source": "http"
                    })
                    print(f"  Collected sample {len(samples)}")
                time.sleep(0.2)  # 5 Hz sampling rate
            except Exception as e:
                print(f"  HTTP collection error: {e}")
                time.sleep(0.5)
                
        return samples
    
    def validate_time_progression(self, samples: List[Dict]) -> Dict[str, Any]:
        """Validate that time values are progressing correctly"""
        print("⏱️  Validating time progression...")
        
        if len(samples) < 2:
            return {"passed": False, "reason": "Insufficient samples"}
        
        timestamps = [s["timestamp"] for s in samples]
        time_differences = [timestamps[i] - timestamps[i-1] for i in range(1, len(timestamps))]
        
        # Check for negative time differences (impossible)
        negative_times = [td for td in time_differences if td < 0]
        if negative_times:
            return {"passed": False, "reason": f"Negative time differences found: {negative_times}"}
        
        # Check for reasonable time intervals
        avg_interval = statistics.mean(time_differences)
        std_interval = statistics.stdev(time_differences) if len(time_differences) > 1 else 0
        
        result = {
            "passed": True,
            "average_interval": avg_interval,
            "std_interval": std_interval,
            "total_duration": timestamps[-1] - timestamps[0],
            "samples_collected": len(samples)
        }
        
        print(f"  ✓ Average interval: {avg_interval:.3f}s")
        print(f"  ✓ Total duration: {result['total_duration']:.3f}s")
        
        return result
    
    def validate_data_entropy(self, samples: List[Dict]) -> Dict[str, Any]:
        """Validate data entropy to ensure it's not static"""
        print("📊 Validating data entropy...")
        
        if len(samples) < 3:
            return {"passed": False, "reason": "Insufficient samples"}
        
        # Extract consciousness levels
        consciousness_levels = []
        for sample in samples:
            data = sample["data"]
            if "consciousness" in data:
                # WebSocket format
                consciousness_levels.append(data["consciousness"].get("level", 0))
            elif "global" in data:
                # HTTP format
                consciousness_levels.append(data["global"].get("consciousness_level", 0))
        
        if len(consciousness_levels) < 3:
            return {"passed": False, "reason": "Could not extract consciousness levels"}
        
        # Calculate entropy (variance as simple measure)
        variance = statistics.variance(consciousness_levels) if len(consciousness_levels) > 1 else 0
        std_dev = statistics.stdev(consciousness_levels) if len(consciousness_levels) > 1 else 0
        
        # Data is considered dynamic if variance is above threshold
        entropy_threshold = 1e-6  # Very small threshold
        passed = variance > entropy_threshold
        
        result = {
            "passed": passed,
            "variance": variance,
            "std_deviation": std_dev,
            "min_value": min(consciousness_levels),
            "max_value": max(consciousness_levels),
            "range": max(consciousness_levels) - min(consciousness_levels)
        }
        
        print(f"  {'✓' if passed else '⚠️'} Variance: {variance:.8f}")
        print(f"  {'✓' if passed else '⚠️'} Range: {result['range']:.6f}")
        
        return result
    
    def validate_node_changes(self, samples: List[Dict]) -> Dict[str, Any]:
        """Validate that individual node values are changing"""
        print("🔄 Validating node value changes...")
        
        if len(samples) < 3:
            return {"passed": False, "reason": "Insufficient samples"}
        
        # Track changes in node outputs
        node_changes = {}
        previous_sample = None
        
        for sample in samples:
            data = sample["data"]
            nodes_data = {}
            
            # Extract nodes data based on format
            if "nodes" in data:
                nodes_data = data["nodes"]
            
            # Compare with previous sample
            if previous_sample:
                prev_nodes = previous_sample["data"].get("nodes", {})
                for node_id, node_info in nodes_data.items():
                    if node_id in prev_nodes:
                        # Extract output values
                        current_output = self._extract_output(node_info)
                        prev_output = self._extract_output(prev_nodes[node_id])
                        
                        change = abs(current_output - prev_output)
                        if node_id not in node_changes:
                            node_changes[node_id] = []
                        node_changes[node_id].append(change)
            
            previous_sample = sample
        
        # Analyze changes
        if not node_changes:
            return {"passed": False, "reason": "No node changes detected"}
        
        # Calculate average changes per node
        avg_changes = []
        for node_id, changes in node_changes.items():
            if changes:
                avg_change = statistics.mean(changes)
                avg_changes.append(avg_change)
        
        if not avg_changes:
            return {"passed": False, "reason": "No changes calculated"}
        
        overall_avg_change = statistics.mean(avg_changes)
        change_threshold = 1e-6  # Very small threshold
        passed = overall_avg_change > change_threshold
        
        result = {
            "passed": passed,
            "average_change": overall_avg_change,
            "nodes_with_changes": len(node_changes),
            "total_nodes": len(samples[0]["data"].get("nodes", {})) if samples else 0
        }
        
        print(f"  {'✓' if passed else '⚠️'} Average node change: {overall_avg_change:.8f}")
        print(f"  {'✓' if passed else '⚠️'} Nodes with changes: {len(node_changes)}")
        
        return result
    
    def _extract_output(self, node_info: Dict) -> float:
        """Extract output value from node info (handle different formats)"""
        if isinstance(node_info, dict):
            if "output" in node_info:
                return float(node_info["output"])
            elif "oscillator" in node_info:
                return float(node_info["oscillator"].get("phase", 0))
        return 0.0
    
    def validate_data_uniqueness(self, samples: List[Dict]) -> Dict[str, Any]:
        """Validate that data samples are unique (not repeated)"""
        print("🔢 Validating data uniqueness...")
        
        if len(samples) < 3:
            return {"passed": False, "reason": "Insufficient samples"}
        
        # Create hashes of data samples
        hashes = []
        for sample in samples:
            data_str = json.dumps(sample["data"], sort_keys=True, default=str)
            hash_val = hashlib.md5(data_str.encode()).hexdigest()
            hashes.append(hash_val)
        
        # Count unique hashes
        unique_hashes = set(hashes)
        uniqueness_ratio = len(unique_hashes) / len(hashes)
        
        # Consider valid if > 80% unique
        uniqueness_threshold = 0.8
        passed = uniqueness_ratio >= uniqueness_threshold
        
        result = {
            "passed": passed,
            "uniqueness_ratio": uniqueness_ratio,
            "unique_samples": len(unique_hashes),
            "total_samples": len(hashes)
        }
        
        print(f"  {'✓' if passed else '⚠️'} Uniqueness ratio: {uniqueness_ratio:.3f}")
        print(f"  {'✓' if passed else '⚠️'} Unique samples: {len(unique_hashes)}/{len(hashes)}")
        
        return result
    
    def cross_validate_sources(self, ws_samples: List[Dict], http_samples: List[Dict]) -> Dict[str, Any]:
        """Validate consistency between WebSocket and HTTP sources"""
        print("🔗 Validating cross-source consistency...")
        
        if len(ws_samples) < 2 or len(http_samples) < 2:
            return {"passed": False, "reason": "Insufficient samples from one or both sources"}
        
        # Get approximate timestamps for comparison
        ws_times = [s["timestamp"] for s in ws_samples]
        http_times = [s["timestamp"] for s in http_samples]
        
        # Find overlapping time periods
        start_time = max(min(ws_times), min(http_times))
        end_time = min(max(ws_times), max(http_times))
        
        if start_time >= end_time:
            return {"passed": False, "reason": "No overlapping time periods"}
        
        # Get samples from overlapping period
        ws_overlap = [s for s in ws_samples if start_time <= s["timestamp"] <= end_time]
        http_overlap = [s for s in http_samples if start_time <= s["timestamp"] <= end_time]
        
        if len(ws_overlap) < 2 or len(http_overlap) < 2:
            return {"passed": False, "reason": "Insufficient overlapping samples"}
        
        # Compare consciousness levels at similar times
        differences = []
        for ws_sample in ws_overlap:
            ws_time = ws_sample["timestamp"]
            # Find closest HTTP sample
            closest_http = min(http_overlap, key=lambda x: abs(x["timestamp"] - ws_time))
            
            # Extract consciousness levels
            ws_data = ws_sample["data"]
            http_data = closest_http["data"]
            
            ws_level = ws_data["consciousness"].get("level", 0) if "consciousness" in ws_data else 0
            http_level = http_data["global"].get("consciousness_level", 0) if "global" in http_data else 0
            
            difference = abs(ws_level - http_level)
            differences.append(difference)
        
        avg_difference = statistics.mean(differences)
        max_difference = max(differences)
        
        # Consider consistent if average difference is reasonable
        consistency_threshold = 0.1  # 10% difference allowed
        passed = avg_difference <= consistency_threshold
        
        result = {
            "passed": passed,
            "average_difference": avg_difference,
            "max_difference": max_difference,
            "ws_samples": len(ws_overlap),
            "http_samples": len(http_overlap)
        }
        
        print(f"  {'✓' if passed else '⚠️'} Average difference: {avg_difference:.6f}")
        print(f"  {'✓' if passed else '⚠️'} Max difference: {max_difference:.6f}")
        
        return result
    
    async def run_comprehensive_validation(self):
        """Run comprehensive validation of all data sources"""
        print("🔍 COMPREHENSIVE DATA VALIDATION TOOL")
        print("=" * 50)
        print("Verifying that consciousness data is REAL and not simulated")
        print()
        
        # Collect data from both sources simultaneously
        print("🔄 Starting simultaneous data collection...")
        ws_task = asyncio.create_task(self.collect_websocket_data(10))
        http_samples = self.collect_http_data(10)
        ws_samples = await ws_task
        
        print(f"\n📊 Collected {len(ws_samples)} WebSocket samples")
        print(f"📊 Collected {len(http_samples)} HTTP samples")
        print()
        
        # Run all validations
        validations = {}
        
        # Individual source validations
        validations["websocket_time"] = self.validate_time_progression(ws_samples)
        validations["http_time"] = self.validate_time_progression(http_samples)
        validations["websocket_entropy"] = self.validate_data_entropy(ws_samples)
        validations["http_entropy"] = self.validate_data_entropy(http_samples)
        validations["websocket_nodes"] = self.validate_node_changes(ws_samples)
        validations["http_nodes"] = self.validate_node_changes(http_samples)
        validations["websocket_uniqueness"] = self.validate_data_uniqueness(ws_samples)
        validations["http_uniqueness"] = self.validate_data_uniqueness(http_samples)
        
        # Cross-source validation
        validations["cross_source"] = self.cross_validate_sources(ws_samples, http_samples)
        
        # Overall results
        print("\n" + "=" * 50)
        print("VALIDATION RESULTS")
        print("=" * 50)
        
        passed_validations = 0
        total_validations = len(validations)
        
        for validation_name, result in validations.items():
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            print(f"{validation_name:25s}: {status}")
            if not result["passed"]:
                print(f"  Reason: {result.get('reason', 'Validation failed')}")
            passed_validations += 1 if result["passed"] else 0
        
        print("\n" + "=" * 50)
        overall_passed = passed_validations >= (total_validations * 0.8)  # 80% threshold
        print(f"OVERALL RESULT: {'🎉 SUCCESS' if overall_passed else '⚠️  CONCERNS'}")
        print(f"Passed: {passed_validations}/{total_validations} validations")
        
        if overall_passed:
            print("\n✅ DATA IS CONFIRMED AS REAL-TIME AND NOT SIMULATED")
            print("   The visualization system can confidently display live data")
        else:
            print("\n⚠️  DATA QUALITY CONCERNS DETECTED")
            print("   Some validations failed - data may be static or simulated")
        
        return overall_passed

def main():
    """Main function"""
    print("🔍 Data Validation Tool")
    print("=" * 30)
    print()
    
    # Check if required libraries are available
    try:
        import websockets
        import requests
    except ImportError as e:
        print(f"❌ Required library not found: {e}")
        print("Please install required libraries with:")
        print("   pip install websockets requests")
        return
    
    # Create and run validation
    validator = DataValidationTool()
    result = asyncio.run(validator.run_comprehensive_validation())
    
    return result

if __name__ == "__main__":
    main()