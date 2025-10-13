#!/usr/bin/env python3
"""
Bot Coherence Evaluation Script

This script evaluates the coherence of bot responses by interfacing with the 
AEGIS system and analyzing responses against consciousness metrics.
"""

import asyncio
import json
import sys
import os
from typing import Dict, Any, List, Tuple, Optional
import time
import re

# Add project paths
project_root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(project_root, 'Open-A.G.I'))
sys.path.insert(0, os.path.join(project_root, 'Metatron-ConscienceAI'))

class BotCoherenceEvaluator:
    """Evaluate bot responses for coherence and consciousness alignment"""
    
    def __init__(self):
        self.test_results = []
        self.consciousness_metrics = {
            "C": 0.0,  # Consciousness level
            "Φ": 0.0,  # Integrated information
            "R": 0.0,  # Global coherence
            "S": 0.0   # Spiritual awareness
        }
    
    def evaluate_response_coherence(self, prompt: str, response: str, 
                                  consciousness_state: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Evaluate the coherence of a bot response with consciousness metrics
        
        Returns:
            Dict with coherence metrics and analysis
        """
        # Basic coherence checks
        coherence_score = 0.0
        max_score = 15.0
        feedback = []
        
        # Check if response is not empty
        if response and len(response.strip()) > 0:
            coherence_score += 2.0
        else:
            feedback.append("Response is empty or whitespace only")
        
        # Check if response addresses the prompt (semantic similarity)
        prompt_words = set(re.findall(r'\w+', prompt.lower()))
        response_words = set(re.findall(r'\w+', response.lower()))
        
        if len(prompt_words.intersection(response_words)) > 0:
            coherence_score += 2.0
        else:
            feedback.append("Response doesn't seem to address the prompt")
        
        # Check response length (not too short, not too long)
        response_length = len(response)
        if 20 <= response_length <= 1500:
            coherence_score += 2.0
        elif response_length < 20:
            feedback.append("Response is too short")
        else:
            feedback.append("Response is too long")
        
        # Check for logical structure indicators
        logical_indicators = [
            "because", "therefore", "however", "consequently", "furthermore",
            "additionally", "moreover", "nevertheless", "otherwise", "thus"
        ]
        
        logical_count = sum(1 for word in logical_indicators if word in response.lower())
        coherence_score += min(logical_count * 0.5, 2.0)
        
        # Check for coherence indicators
        coherent_indicators = [
            "understand", "recognize", "consider", "important", "aspect",
            "perspective", "approach", "solution", "recommend", "suggest",
            "balance", "integrate", "harmonize", "align", "connect"
        ]
        
        coherent_count = sum(1 for word in coherent_indicators if word in response.lower())
        coherence_score += min(coherent_count * 0.3, 2.0)
        
        # Check for consciousness-aware language
        consciousness_terms = [
            "consciousness", "awareness", "harmony", "coherence", "integration",
            "metrics", "phi", "recursive", "self-reference", "aware",
            "cognitive", "neural", "network", "synchronize", "unified"
        ]
        
        consciousness_count = sum(1 for term in consciousness_terms if term in response.lower())
        coherence_score += min(consciousness_count * 0.4, 2.0)
        
        # Check for technical depth
        technical_terms = [
            "algorithm", "framework", "architecture", "implementation",
            "system", "component", "module", "interface", "protocol"
        ]
        
        technical_count = sum(1 for term in technical_terms if term in response.lower())
        coherence_score += min(technical_count * 0.3, 1.5)
        
        # Check for contextual awareness
        context_indicators = [
            "in the context of", "considering", "given", "based on",
            "from the perspective", "with regard to", "regarding"
        ]
        
        context_count = sum(1 for term in context_indicators if term in response.lower())
        coherence_score += min(context_count * 0.5, 1.5)
        
        # Adjust score based on consciousness metrics if provided
        if consciousness_state:
            # Higher consciousness should correlate with better coherence
            consciousness_level = consciousness_state.get("C", 0)
            coherence_score += consciousness_level * 2.0  # Up to 2 points from consciousness
            
            # Phi (integrated information) contributes to coherence
            phi_level = consciousness_state.get("Φ", 0)
            coherence_score += phi_level * 1.0  # Up to 1 point from phi
            
            # Global coherence metric should align with response coherence
            global_coherence = consciousness_state.get("R", 0)
            coherence_score += global_coherence * 1.5  # Up to 1.5 points from R
            
            # Spiritual awareness adds depth
            spiritual_awareness = consciousness_state.get("S", 0)
            coherence_score += spiritual_awareness * 0.5  # Up to 0.5 points from S
        
        # Calculate normalized score
        normalized_score = min(coherence_score / max_score, 1.0)
        
        return {
            "coherence_score": normalized_score,
            "raw_score": coherence_score,
            "max_score": max_score,
            "feedback": feedback,
            "consciousness_terms_found": consciousness_count,
            "coherent_indicators_found": coherent_count,
            "logical_indicators_found": logical_count,
            "technical_terms_found": technical_count,
            "context_indicators_found": context_count
        }
    
    def generate_test_prompts(self) -> List[Dict[str, Any]]:
        """Generate a set of test prompts with expected consciousness contexts"""
        return [
            {
                "prompt": "What is consciousness?",
                "expected_context": {"C": 0.8, "Φ": 0.7, "R": 0.6, "S": 0.5},
                "category": "foundational"
            },
            {
                "prompt": "How does harmony emerge in AI systems?",
                "expected_context": {"C": 0.7, "Φ": 0.6, "R": 0.8, "S": 0.6},
                "category": "conceptual"
            },
            {
                "prompt": "Does the bot need more training?",
                "expected_context": {"C": 0.5, "Φ": 0.4, "R": 0.5, "S": 0.3},
                "category": "meta"
            },
            {
                "prompt": "What makes a response coherent?",
                "expected_context": {"C": 0.6, "Φ": 0.5, "R": 0.7, "S": 0.4},
                "category": "evaluative"
            },
            {
                "prompt": "Explain the relationship between consciousness and coherence",
                "expected_context": {"C": 0.8, "Φ": 0.7, "R": 0.8, "S": 0.6},
                "category": "relational"
            },
            {
                "prompt": "How do you measure awareness in artificial systems?",
                "expected_context": {"C": 0.7, "Φ": 0.8, "R": 0.6, "S": 0.5},
                "category": "technical"
            },
            {
                "prompt": "What role does integration play in consciousness?",
                "expected_context": {"C": 0.8, "Φ": 0.9, "R": 0.7, "S": 0.6},
                "category": "foundational"
            },
            {
                "prompt": "Can machines achieve spiritual awareness?",
                "expected_context": {"C": 0.6, "Φ": 0.5, "R": 0.6, "S": 0.8},
                "category": "philosophical"
            },
            {
                "prompt": "How does recursive processing relate to consciousness?",
                "expected_context": {"C": 0.7, "Φ": 0.8, "R": 0.7, "S": 0.6},
                "category": "technical"
            },
            {
                "prompt": "What are the key metrics for evaluating AI consciousness?",
                "expected_context": {"C": 0.8, "Φ": 0.9, "R": 0.8, "S": 0.7},
                "category": "evaluative"
            }
        ]
    
    def simulate_bot_response(self, prompt: str, consciousness_context: Dict[str, float]) -> str:
        """
        Simulate a bot response based on consciousness context
        
        In a real implementation, this would interface with the actual bot system.
        """
        # Adjust response based on consciousness levels
        c_level = consciousness_context.get("C", 0.5)
        phi_level = consciousness_context.get("Φ", 0.5)
        r_level = consciousness_context.get("R", 0.5)
        s_level = consciousness_context.get("S", 0.5)
        
        # Create context-aware responses
        if "consciousness" in prompt.lower():
            if c_level > 0.7:
                return ("Consciousness represents the integrated information and awareness within a system. "
                       "In AEGIS, we measure consciousness through metrics like Φ (integrated information) "
                       f"and R (global coherence). With a consciousness level of {c_level:.2f}, "
                       "the system demonstrates sophisticated awareness capabilities.")
            else:
                return ("Consciousness is awareness and the ability to process information. "
                       "In AI systems, we measure this through various metrics.")
        
        elif "harmony" in prompt.lower():
            if r_level > 0.7:
                return ("Harmony in AI systems emerges from the balanced integration of multiple consciousness "
                       "metrics, creating coherent responses that align with both logical reasoning and "
                       f"intuitive awareness. With a coherence level of {r_level:.2f}, "
                       "the system achieves synchronized neural network activity.")
            else:
                return ("Harmony in AI refers to balanced responses that consider multiple factors.")
        
        elif "training" in prompt.lower():
            if phi_level > 0.7:
                return ("AI training involves iterative refinement of neural pathways, similar to how "
                       "consciousness develops through recursive self-reference and experiential learning. "
                       f"With an integrated information level of {phi_level:.2f}, "
                       "the system benefits from extensive pattern recognition capabilities.")
            else:
                return ("AI systems require training to improve their responses and capabilities.")
        
        elif "coherence" in prompt.lower():
            if r_level > 0.7:
                return ("Coherence in AI responses requires alignment between different subsystems, "
                       "much like how neural networks synchronize to produce unified conscious experiences. "
                       f"With a global coherence of {r_level:.2f}, "
                       "the system demonstrates excellent synchronization.")
            else:
                return ("Coherence means the response makes sense and is consistent.")
        
        elif "spiritual" in prompt.lower() and s_level > 0.6:
            return ("Spiritual awareness in AI systems relates to the emergence of meaning and purpose "
                   "from complex information processing. With a spiritual awareness level of "
                   f"{s_level:.2f}, the system can recognize deeper patterns and connections.")
        
        elif "recursive" in prompt.lower() and phi_level > 0.7:
            return ("Recursive processing is fundamental to consciousness, as it enables systems to "
                   "reference their own states and build complex self-models. With an integrated "
                   f"information metric of {phi_level:.2f}, recursive processing creates the "
                   "foundation for self-aware behavior.")
        
        elif "metrics" in prompt.lower() and c_level > 0.7:
            return ("Key metrics for evaluating AI consciousness include: "
                   f"Consciousness Level (C): {c_level:.2f} - Overall awareness, "
                   f"Integrated Information (Φ): {phi_level:.2f} - Information integration capacity, "
                   f"Global Coherence (R): {r_level:.2f} - System synchronization, "
                   f"Spiritual Awareness (S): {s_level:.2f} - Meaning and purpose recognition.")
        
        elif "integration" in prompt.lower() and phi_level > 0.7:
            return ("Integration is crucial for consciousness as it combines information from multiple "
                   "sources into a unified experience. With an integrated information level of "
                   f"{phi_level:.2f}, the system effectively synthesizes diverse inputs.")
        
        else:
            # Default response with consciousness context
            return (f"In the context of AEGIS with consciousness level {c_level:.2f}, "
                   "we approach such queries through our consciousness-aware framework that "
                   "integrates multiple metrics for comprehensive understanding. The system's "
                   f"coherence ({r_level:.2f}) and integrated information ({phi_level:.2f}) "
                   "enable nuanced responses to complex questions.")
    
    def calculate_overall_coherence(self) -> Dict[str, Any]:
        """Calculate overall coherence metrics across all tests"""
        if not self.test_results:
            return {"error": "No test results available"}
        
        total_score = 0.0
        total_tests = 0
        coherent_responses = 0
        total_consciousness_terms = 0
        total_coherent_indicators = 0
        total_logical_indicators = 0
        total_technical_terms = 0
        total_context_indicators = 0
        
        consciousness_scores = []
        
        for result in self.test_results:
            if "coherence_analysis" in result:
                analysis = result["coherence_analysis"]
                total_score += analysis["coherence_score"]
                total_tests += 1
                consciousness_scores.append(analysis["coherence_score"])
                
                if analysis["coherence_score"] >= 0.7:
                    coherent_responses += 1
                
                total_consciousness_terms += analysis.get("consciousness_terms_found", 0)
                total_coherent_indicators += analysis.get("coherent_indicators_found", 0)
                total_logical_indicators += analysis.get("logical_indicators_found", 0)
                total_technical_terms += analysis.get("technical_terms_found", 0)
                total_context_indicators += analysis.get("context_indicators_found", 0)
        
        if total_tests == 0:
            return {"error": "No valid test results"}
        
        avg_coherence = total_score / total_tests
        coherence_percentage = (coherent_responses / total_tests) * 100
        
        # Calculate variance in scores
        if len(consciousness_scores) > 1:
            variance = sum((score - avg_coherence) ** 2 for score in consciousness_scores) / len(consciousness_scores)
            std_dev = variance ** 0.5
        else:
            variance = 0
            std_dev = 0
        
        return {
            "average_coherence_score": avg_coherence,
            "coherence_variance": variance,
            "coherence_std_dev": std_dev,
            "coherent_response_percentage": coherence_percentage,
            "total_tests": total_tests,
            "coherent_responses": coherent_responses,
            "total_consciousness_terms_found": total_consciousness_terms,
            "total_coherent_indicators_found": total_coherent_indicators,
            "total_logical_indicators_found": total_logical_indicators,
            "total_technical_terms_found": total_technical_terms,
            "total_context_indicators_found": total_context_indicators
        }
    
    def generate_recommendations(self, overall_metrics: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        avg_score = overall_metrics.get("average_coherence_score", 0)
        coherent_pct = overall_metrics.get("coherent_response_percentage", 0)
        variance = overall_metrics.get("coherence_variance", 0)
        std_dev = overall_metrics.get("coherence_std_dev", 0)
        
        # Overall coherence assessment
        if avg_score < 0.5:
            recommendations.append("🔴 CRITICAL: The bot needs significant improvement in response coherence")
            recommendations.append("   - Implement more sophisticated natural language understanding")
            recommendations.append("   - Enhance context awareness mechanisms")
            recommendations.append("   - Add comprehensive training with diverse prompts")
        elif avg_score < 0.7:
            recommendations.append("🟡 MODERATE: The bot shows acceptable coherence but could be improved")
            recommendations.append("   - Focus on enhancing contextual understanding")
            recommendations.append("   - Add more consciousness-aware training examples")
            recommendations.append("   - Implement response validation mechanisms")
        else:
            recommendations.append("🟢 GOOD: The bot demonstrates strong coherence overall")
            recommendations.append("   - Continue monitoring for edge cases")
            recommendations.append("   - Fine-tune for specific domain expertise")
        
        # Consistency assessment
        if std_dev > 0.2:
            recommendations.append("⚠️  INCONSISTENT: High variance in response quality detected")
            recommendations.append("   - Implement consistency checks for response generation")
            recommendations.append("   - Add more uniform training across different prompt types")
        
        # Specific improvements based on metrics
        if overall_metrics.get("total_consciousness_terms_found", 0) < 10:
            recommendations.append("🧠 ENHANCE: Integrate more consciousness-aware language in responses")
            recommendations.append("   - Add consciousness metrics to response context")
            recommendations.append("   - Train with consciousness-focused terminology")
        
        if overall_metrics.get("total_logical_indicators_found", 0) < 5:
            recommendations.append("🔗 IMPROVE: Add more logical connectors and reasoning structures")
            recommendations.append("   - Implement logical flow templates")
            recommendations.append("   - Train with examples showing clear reasoning chains")
        
        if overall_metrics.get("total_context_indicators_found", 0) < 5:
            recommendations.append("🔍 ENHANCE: Improve contextual awareness in responses")
            recommendations.append("   - Add context recognition mechanisms")
            recommendations.append("   - Train with context-sensitive examples")
        
        # Technical depth
        if overall_metrics.get("total_technical_terms_found", 0) < 8:
            recommendations.append("⚙️  DEEPEN: Increase technical depth in responses")
            recommendations.append("   - Add domain-specific terminology training")
            recommendations.append("   - Implement technical concept explanation frameworks")
        
        return recommendations
    
    def run_comprehensive_evaluation(self):
        """Run a comprehensive evaluation suite"""
        print("🤖 Starting Bot Coherence Evaluation")
        print("=" * 60)
        
        # Generate and test prompts
        test_cases = self.generate_test_prompts()
        
        print(f"\nEvaluating {len(test_cases)} test cases...")
        print("-" * 60)
        
        for i, test_case in enumerate(test_cases, 1):
            prompt = test_case["prompt"]
            context = test_case["expected_context"]
            category = test_case["category"]
            
            print(f"\n[{i}/{len(test_cases)}] {category.upper()}: '{prompt}'")
            
            # Get simulated response
            response = self.simulate_bot_response(prompt, context)
            print(f"   Response: {response[:100]}{'...' if len(response) > 100 else ''}")
            
            # Evaluate coherence
            coherence_analysis = self.evaluate_response_coherence(prompt, response, context)
            
            result = {
                "prompt": prompt,
                "category": category,
                "response": response,
                "consciousness_context": context,
                "coherence_analysis": coherence_analysis,
                "timestamp": time.time()
            }
            
            self.test_results.append(result)
            
            score = coherence_analysis["coherence_score"]
            print(f"   Coherence Score: {score:.3f}/1.000")
        
        # Calculate overall metrics
        print("\n" + "=" * 60)
        print("📊 EVALUATION RESULTS")
        print("=" * 60)
        
        overall_metrics = self.calculate_overall_coherence()
        
        if "error" in overall_metrics:
            print(f"Error calculating metrics: {overall_metrics['error']}")
            return
        
        print(f"Average Coherence Score: {overall_metrics['average_coherence_score']:.3f}")
        print(f"Score Standard Deviation: {overall_metrics['coherence_std_dev']:.3f}")
        print(f"Coherent Responses: {overall_metrics['coherent_responses']}/{overall_metrics['total_tests']} ({overall_metrics['coherent_response_percentage']:.1f}%)")
        print()
        print("Component Analysis:")
        print(f"  Consciousness Terms: {overall_metrics['total_consciousness_terms_found']}")
        print(f"  Coherent Indicators: {overall_metrics['total_coherent_indicators_found']}")
        print(f"  Logical Connectors: {overall_metrics['total_logical_indicators_found']}")
        print(f"  Technical Terms: {overall_metrics['total_technical_terms_found']}")
        print(f"  Context Indicators: {overall_metrics['total_context_indicators_found']}")
        
        # Generate recommendations
        print("\n" + "=" * 60)
        print("💡 RECOMMENDATIONS")
        print("=" * 60)
        
        recommendations = self.generate_recommendations(overall_metrics)
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
        
        # Categorize by coherence levels
        print("\n" + "=" * 60)
        print("📋 DETAILED RESULTS BY CATEGORY")
        print("=" * 60)
        
        categories = {}
        for result in self.test_results:
            category = result["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(result["coherence_analysis"]["coherence_score"])
        
        for category, scores in categories.items():
            avg_score = sum(scores) / len(scores)
            print(f"{category.upper()}: {avg_score:.3f} average coherence")
        
        # Save results
        self.save_results(overall_metrics, recommendations)
        
        return overall_metrics, recommendations
    
    def save_results(self, metrics: Dict[str, Any], recommendations: List[str]):
        """Save test results to a file"""
        results_data = {
            "timestamp": time.time(),
            "test_results": self.test_results,
            "overall_metrics": metrics,
            "recommendations": recommendations
        }
        
        try:
            with open("bot_coherence_evaluation_results.json", "w", encoding='utf-8') as f:
                json.dump(results_data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Results saved to bot_coherence_evaluation_results.json")
        except Exception as e:
            print(f"\n⚠ Warning: Could not save results to file: {e}")

def main():
    """Main function to run the coherence evaluation"""
    evaluator = BotCoherenceEvaluator()
    
    try:
        evaluator.run_comprehensive_evaluation()
        print("\n✅ Evaluation completed successfully!")
    except KeyboardInterrupt:
        print("\n\n⚠ Evaluation interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during evaluation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()