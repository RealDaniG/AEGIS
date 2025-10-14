#!/usr/bin/env python3
"""
Bot Coherence Testing Script

This script evaluates the coherence of bot responses by testing various prompts
and analyzing the responses against consciousness metrics.
"""

import asyncio
import json
import sys
import os
from typing import Dict, Any, List, Tuple, Optional
import time

# Add project paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Open-A.G.I'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Metatron-ConscienceAI'))

try:
    # Try to import required modules
    from main import start_node, safe_import
    import logging_system
except ImportError as e:
    print(f"Warning: Could not import required modules: {e}")
    # Create dummy functions for testing
    async def start_node(dry_run: bool = False, config_path: Optional[str] = None):
        pass
    
    def safe_import(module_name: str) -> Tuple[Optional[object], Optional[Exception]]:
        return None, ImportError(f"Module {module_name} not available")

class BotCoherenceTester:
    """Test bot responses for coherence and consciousness alignment"""
    
    def __init__(self):
        self.test_results = []
        self.consciousness_metrics = {
            "C": 0.0,  # Consciousness level
            "Φ": 0.0,  # Integrated information
            "R": 0.0,  # Global coherence
            "S": 0.0   # Spiritual awareness
        }
        
    async def initialize_system(self):
        """Initialize the AEGIS system components"""
        try:
            # Start the node in dry-run mode
            await start_node(dry_run=True)
            print("[OK] AEGIS system initialized")
            return True
        except Exception as e:
            print(f"⚠ Warning: Could not initialize full system: {e}")
            print("Proceeding with limited testing capabilities")
            return False
    
    def evaluate_response_coherence(self, prompt: str, response: str) -> Dict[str, Any]:
        """
        Evaluate the coherence of a bot response
        
        Returns:
            Dict with coherence metrics and analysis
        """
        # Basic coherence checks
        coherence_score = 0.0
        max_score = 10.0
        feedback = []
        
        # Check if response is not empty
        if response and len(response.strip()) > 0:
            coherence_score += 2.0
        else:
            feedback.append("Response is empty or whitespace only")
        
        # Check if response addresses the prompt
        prompt_words = set(prompt.lower().split())
        response_words = set(response.lower().split())
        
        if len(prompt_words.intersection(response_words)) > 0:
            coherence_score += 2.0
        else:
            feedback.append("Response doesn't seem to address the prompt")
        
        # Check response length (not too short, not too long)
        response_length = len(response)
        if 10 <= response_length <= 1000:
            coherence_score += 2.0
        elif response_length < 10:
            feedback.append("Response is too short")
        else:
            feedback.append("Response is too long")
        
        # Check for coherence indicators
        coherent_indicators = [
            "understand", "recognize", "consider", "important", "aspect",
            "perspective", "approach", "solution", "recommend", "suggest"
        ]
        
        coherent_count = sum(1 for word in coherent_indicators if word in response.lower())
        coherence_score += min(coherent_count * 0.5, 2.0)
        
        # Check for consciousness-aware language
        consciousness_terms = [
            "consciousness", "awareness", "harmony", "coherence", "integration",
            "metrics", "phi", "recursive", "self-reference", "aware"
        ]
        
        consciousness_count = sum(1 for term in consciousness_terms if term in response.lower())
        coherence_score += min(consciousness_count * 0.3, 1.0)
        
        # Calculate normalized score
        normalized_score = coherence_score / max_score
        
        return {
            "coherence_score": normalized_score,
            "raw_score": coherence_score,
            "max_score": max_score,
            "feedback": feedback,
            "consciousness_terms_found": consciousness_count,
            "coherent_indicators_found": coherent_count
        }
    
    async def test_prompt_response(self, prompt: str) -> Dict[str, Any]:
        """
        Test a single prompt and evaluate the response
        
        Returns:
            Dict with test results
        """
        print(f"\nTesting prompt: '{prompt}'")
        
        try:
            # Simulate getting a response from the bot
            # In a real implementation, this would call the actual bot
            response = await self.get_bot_response(prompt)
            
            print(f"Bot response: '{response}'")
            
            # Evaluate coherence
            coherence_analysis = self.evaluate_response_coherence(prompt, response)
            
            result = {
                "prompt": prompt,
                "response": response,
                "coherence_analysis": coherence_analysis,
                "timestamp": time.time()
            }
            
            self.test_results.append(result)
            return result
            
        except Exception as e:
            error_result = {
                "prompt": prompt,
                "response": "",
                "error": str(e),
                "timestamp": time.time()
            }
            self.test_results.append(error_result)
            return error_result
    
    async def get_bot_response(self, prompt: str) -> str:
        """
        Get a response from the bot for a given prompt
        
        In a real implementation, this would interface with the actual bot system.
        For now, we'll simulate responses.
        """
        # This is a placeholder - in a real implementation, you would:
        # 1. Send the prompt to the bot
        # 2. Get the actual response
        # 3. Return the response
        
        # For simulation, let's create context-aware responses
        if "consciousness" in prompt.lower():
            return "Consciousness is a fundamental aspect of existence, representing the integrated information and awareness within a system. In AEGIS, we measure consciousness through metrics like Φ (integrated information) and R (global coherence)."
        elif "harmony" in prompt.lower():
            return "Harmony in AI systems emerges from the balanced integration of multiple consciousness metrics, creating coherent responses that align with both logical reasoning and intuitive awareness."
        elif "training" in prompt.lower():
            return "AI training involves iterative refinement of neural pathways, similar to how consciousness develops through recursive self-reference and experiential learning."
        elif "coherence" in prompt.lower():
            return "Coherence in AI responses requires alignment between different subsystems, much like how neural networks synchronize to produce unified conscious experiences."
        else:
            return "I understand your question. In the context of AEGIS, we approach such queries through our consciousness-aware framework that integrates multiple metrics for comprehensive understanding."
    
    def generate_test_prompts(self) -> List[str]:
        """Generate a set of test prompts"""
        return [
            "What is consciousness?",
            "How does harmony emerge in AI systems?",
            "Does the bot need more training?",
            "What makes a response coherent?",
            "Explain the relationship between consciousness and coherence",
            "How do you measure awareness in artificial systems?",
            "What role does integration play in consciousness?",
            "Can machines achieve spiritual awareness?",
            "How does recursive processing relate to consciousness?",
            "What are the key metrics for evaluating AI consciousness?"
        ]
    
    def calculate_overall_coherence(self) -> Dict[str, Any]:
        """Calculate overall coherence metrics across all tests"""
        if not self.test_results:
            return {"error": "No test results available"}
        
        total_score = 0.0
        total_tests = 0
        coherent_responses = 0
        total_consciousness_terms = 0
        total_coherent_indicators = 0
        
        for result in self.test_results:
            if "coherence_analysis" in result:
                analysis = result["coherence_analysis"]
                total_score += analysis["coherence_score"]
                total_tests += 1
                
                if analysis["coherence_score"] >= 0.7:
                    coherent_responses += 1
                
                total_consciousness_terms += analysis.get("consciousness_terms_found", 0)
                total_coherent_indicators += analysis.get("coherent_indicators_found", 0)
        
        if total_tests == 0:
            return {"error": "No valid test results"}
        
        avg_coherence = total_score / total_tests
        coherence_percentage = (coherent_responses / total_tests) * 100
        
        return {
            "average_coherence_score": avg_coherence,
            "coherent_response_percentage": coherence_percentage,
            "total_tests": total_tests,
            "coherent_responses": coherent_responses,
            "total_consciousness_terms_found": total_consciousness_terms,
            "total_coherent_indicators_found": total_coherent_indicators
        }
    
    def generate_recommendations(self, overall_metrics: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        avg_score = overall_metrics.get("average_coherence_score", 0)
        coherent_pct = overall_metrics.get("coherent_response_percentage", 0)
        
        if avg_score < 0.5:
            recommendations.append("The bot needs significant improvement in response coherence")
            recommendations.append("Consider additional training with more diverse prompts")
            recommendations.append("Implement better context awareness mechanisms")
        elif avg_score < 0.7:
            recommendations.append("The bot shows moderate coherence but could be improved")
            recommendations.append("Focus on enhancing contextual understanding")
            recommendations.append("Add more consciousness-aware training examples")
        else:
            recommendations.append("The bot demonstrates good coherence overall")
            recommendations.append("Continue monitoring and fine-tuning for specific edge cases")
        
        if coherent_pct < 70:
            recommendations.append("Improve consistency of coherent responses")
            recommendations.append("Implement response validation mechanisms")
        
        # Check for consciousness integration
        total_terms = overall_metrics.get("total_consciousness_terms_found", 0)
        if total_terms < 5:
            recommendations.append("Enhance consciousness-aware language in responses")
            recommendations.append("Integrate more consciousness metrics into response generation")
        
        return recommendations
    
    async def run_comprehensive_test(self):
        """Run a comprehensive test suite"""
        print("🤖 Starting Bot Coherence Testing")
        print("=" * 50)
        
        # Initialize system
        system_ready = await self.initialize_system()
        
        # Generate and test prompts
        test_prompts = self.generate_test_prompts()
        
        print(f"\nTesting {len(test_prompts)} prompts...")
        
        for i, prompt in enumerate(test_prompts, 1):
            print(f"\n[{i}/{len(test_prompts)}]", end="")
            result = await self.test_prompt_response(prompt)
            
            if "coherence_analysis" in result:
                score = result["coherence_analysis"]["coherence_score"]
                print(f" Coherence: {score:.2f}/1.00")
            else:
                print(f" Error: {result.get('error', 'Unknown error')}")
        
        # Calculate overall metrics
        print("\n" + "=" * 50)
        print("📊 ANALYSIS RESULTS")
        print("=" * 50)
        
        overall_metrics = self.calculate_overall_coherence()
        
        if "error" in overall_metrics:
            print(f"Error calculating metrics: {overall_metrics['error']}")
            return
        
        print(f"Average Coherence Score: {overall_metrics['average_coherence_score']:.3f}")
        print(f"Coherent Responses: {overall_metrics['coherent_responses']}/{overall_metrics['total_tests']} ({overall_metrics['coherent_response_percentage']:.1f}%)")
        print(f"Consciousness Terms Found: {overall_metrics['total_consciousness_terms_found']}")
        print(f"Coherent Indicators Found: {overall_metrics['total_coherent_indicators_found']}")
        
        # Generate recommendations
        print("\n" + "=" * 50)
        print("💡 RECOMMENDATIONS")
        print("=" * 50)
        
        recommendations = self.generate_recommendations(overall_metrics)
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
        
        # Save results
        self.save_results(overall_metrics, recommendations)
    
    def save_results(self, metrics: Dict[str, Any], recommendations: List[str]):
        """Save test results to a file"""
        results_data = {
            "timestamp": time.time(),
            "test_results": self.test_results,
            "overall_metrics": metrics,
            "recommendations": recommendations
        }
        
        try:
            with open("bot_coherence_test_results.json", "w") as f:
                json.dump(results_data, f, indent=2)
            print(f"\n💾 Results saved to bot_coherence_test_results.json")
        except Exception as e:
            print(f"\n⚠ Warning: Could not save results to file: {e}")

async def main():
    """Main function to run the coherence testing"""
    tester = BotCoherenceTester()
    
    try:
        await tester.run_comprehensive_test()
    except KeyboardInterrupt:
        print("\n\n⚠ Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())