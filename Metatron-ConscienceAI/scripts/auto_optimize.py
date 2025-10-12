#!/usr/bin/env python
"""
Auto-Optimization for ConscienceAI
==================================

Automatically optimizes chat parameters based on performance metrics
and user feedback, similar to KaseMaster's approach.

Features:
- Parameter tuning based on response quality
- Performance monitoring
- Automatic adjustment of chat settings
- Scheduled optimization
"""

import os
import json
import time
import argparse
from pathlib import Path
from typing import Dict, Any, List
import requests


class ChatOptimizer:
    def __init__(self, server_url: str = "http://localhost:5180"):
        """
        Initialize chat optimizer.
        
        Args:
            server_url: URL of the chat server
        """
        self.server_url = server_url
        self.optimization_log = []
        self.best_params = {
            "temperature": 0.7,
            "max_new_tokens": 128,
            "top_k": 50,
            "top_p": 0.9,
            "repetition_penalty": 1.2
        }
        self.performance_history = []
    
    def test_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Test chat parameters and evaluate performance.
        
        Args:
            params: Dictionary of parameters to test
            
        Returns:
            Dictionary with test results
        """
        try:
            # Test prompt
            test_prompt = "Explain the concept of artificial intelligence in one sentence."
            
            # Send request to chat server
            response = requests.post(
                f"{self.server_url}/api/chat",
                json={
                    "message": test_prompt,
                    "max_new_tokens": params.get("max_new_tokens", 128),
                    "temperature": params.get("temperature", 0.7)
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "")
                
                # Evaluate response quality (simplified)
                quality_score = self._evaluate_response_quality(response_text)
                response_time = response.elapsed.total_seconds()
                
                result = {
                    "success": True,
                    "response_time": response_time,
                    "quality_score": quality_score,
                    "response_length": len(response_text),
                    "params": params
                }
            else:
                result = {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "params": params
                }
                
        except Exception as e:
            result = {
                "success": False,
                "error": str(e),
                "params": params
            }
        
        self.optimization_log.append({
            "timestamp": time.time(),
            "test_result": result
        })
        
        return result
    
    def _evaluate_response_quality(self, response: str) -> float:
        """
        Evaluate response quality (simplified scoring).
        
        Args:
            response: Response text to evaluate
            
        Returns:
            Quality score between 0.0 and 1.0
        """
        if not response:
            return 0.0
        
        # Simple heuristics for quality scoring
        word_count = len(response.split())
        char_count = len(response)
        
        # Prefer responses of moderate length
        if word_count < 5:
            length_score = 0.3
        elif word_count < 20:
            length_score = 1.0
        elif word_count < 50:
            length_score = 0.8
        else:
            length_score = 0.5
        
        # Prefer responses without excessive repetition
        unique_chars = len(set(response.lower()))
        repetition_score = min(1.0, unique_chars / max(1, char_count))
        
        # Combined score
        quality = 0.6 * length_score + 0.4 * repetition_score
        return max(0.0, min(1.0, quality))
    
    def optimize_parameters(self, iterations: int = 10) -> Dict[str, Any]:
        """
        Optimize chat parameters through testing.
        
        Args:
            iterations: Number of optimization iterations
            
        Returns:
            Dictionary with optimization results
        """
        print("Starting parameter optimization...")
        print(f"Testing {iterations} parameter combinations")
        
        best_score = 0.0
        best_params = self.best_params.copy()
        
        # Parameter ranges for testing
        param_ranges = {
            "temperature": [0.3, 0.5, 0.7, 0.9, 1.1],
            "max_new_tokens": [64, 128, 256, 512],
            "top_k": [10, 25, 50, 100],
            "top_p": [0.8, 0.9, 0.95, 0.99]
        }
        
        test_count = 0
        for temp in param_ranges["temperature"]:
            for tokens in param_ranges["max_new_tokens"]:
                for top_k in param_ranges["top_k"]:
                    for top_p in param_ranges["top_p"]:
                        if test_count >= iterations:
                            break
                        
                        params = {
                            "temperature": temp,
                            "max_new_tokens": tokens,
                            "top_k": top_k,
                            "top_p": top_p
                        }
                        
                        print(f"Testing parameters: {params}")
                        result = self.test_parameters(params)
                        
                        if result["success"]:
                            # Combined score (response time and quality)
                            time_score = max(0.1, 1.0 - result["response_time"] / 5.0)
                            combined_score = 0.4 * result["quality_score"] + 0.6 * time_score
                            
                            if combined_score > best_score:
                                best_score = combined_score
                                best_params = params.copy()
                                print(f"New best score: {best_score:.3f}")
                        
                        test_count += 1
                        time.sleep(0.5)  # Small delay between tests
        
        self.best_params = best_params
        optimization_result = {
            "best_params": best_params,
            "best_score": best_score,
            "tests_run": test_count,
            "completed_at": time.time()
        }
        
        self.performance_history.append(optimization_result)
        print(f"Optimization complete. Best parameters: {best_params}")
        return optimization_result
    
    def save_settings(self, filepath: str = "ai_runs/webchat_settings.json") -> bool:
        """
        Save optimized settings to file.
        
        Args:
            filepath: Path to save settings file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            path = Path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save settings
            settings = {
                "optimized_params": self.best_params,
                "last_optimization": time.time(),
                "performance_history": self.performance_history[-10:]  # Last 10 entries
            }
            
            with open(filepath, "w") as f:
                json.dump(settings, f, indent=2)
            
            print(f"Settings saved to: {filepath}")
            return True
            
        except Exception as e:
            print(f"Failed to save settings: {e}")
            return False
    
    def load_settings(self, filepath: str = "ai_runs/webchat_settings.json") -> bool:
        """
        Load settings from file.
        
        Args:
            filepath: Path to settings file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not Path(filepath).exists():
                print(f"Settings file not found: {filepath}")
                return False
            
            with open(filepath, "r") as f:
                settings = json.load(f)
            
            self.best_params = settings.get("optimized_params", self.best_params)
            self.performance_history = settings.get("performance_history", [])
            
            print(f"Settings loaded from: {filepath}")
            return True
            
        except Exception as e:
            print(f"Failed to load settings: {e}")
            return False
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance report."""
        if not self.performance_history:
            return {"message": "No performance data available"}
        
        latest = self.performance_history[-1]
        avg_score = sum(h.get("best_score", 0) for h in self.performance_history) / len(self.performance_history)
        
        return {
            "latest_optimization": latest,
            "average_score": avg_score,
            "total_optimizations": len(self.performance_history),
            "current_params": self.best_params
        }


def main():
    """Main function for auto-optimization."""
    parser = argparse.ArgumentParser(description="Auto-optimize ConscienceAI chat parameters")
    parser.add_argument("--server_url", default="http://localhost:5180", help="Chat server URL")
    parser.add_argument("--iterations", type=int, default=10, help="Number of optimization iterations")
    parser.add_argument("--output", default="ai_runs/webchat_settings.json", help="Output settings file")
    parser.add_argument("--load", action="store_true", help="Load existing settings instead of optimizing")
    
    args = parser.parse_args()
    
    print("ConscienceAI Auto-Optimizer")
    print("=" * 40)
    print(f"Server URL: {args.server_url}")
    print(f"Iterations: {args.iterations}")
    print(f"Output file: {args.output}")
    print()
    
    optimizer = ChatOptimizer(server_url=args.server_url)
    
    if args.load:
        # Load existing settings
        if optimizer.load_settings(args.output):
            print("Settings loaded successfully")
        else:
            print("Failed to load settings")
    else:
        # Run optimization
        try:
            result = optimizer.optimize_parameters(iterations=args.iterations)
            optimizer.save_settings(args.output)
            
            print("\nOptimization Results:")
            print(f"Best Score: {result['best_score']:.3f}")
            print(f"Best Parameters: {result['best_params']}")
            print(f"Tests Run: {result['tests_run']}")
            
        except KeyboardInterrupt:
            print("\nOptimization interrupted by user")
        except Exception as e:
            print(f"Optimization failed: {e}")


if __name__ == "__main__":
    main()