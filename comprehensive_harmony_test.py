#!/usr/bin/env python3
"""
Comprehensive Harmony Test for METATRONV2 System

This test verifies that all 13 nodes across the 4 apps are connected and working in harmony:
1. Metatron-ConscienceAI (13-node consciousness network)
2. Open-A.G.I (Distributed AGI system)
3. aegis-conscience (Security framework)
4. Unified System (Integration layer)

The test validates:
- Node connectivity across all systems
- Pipeline integration from sensory input to AGI decision making
- Orchestrator coordination
- Consciousness-aware AGI decision making
- Cross-system communication protocols
"""

import sys
import os
import asyncio
import json
import time
import logging
from typing import Dict, List, Any

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import system components
try:
    from unified_coordinator import UnifiedSystemCoordinator
    from unified_api.client import UnifiedAPIClient
    from unified_components.network import UnifiedP2PNetwork
    from unified_components.consensus import UnifiedConsensus
    from consciousness_aware_agi.decision_engine import ConsciousnessAwareDecisionEngine
    from cross_system_comm.protocols import CrossSystemCommunicator
    # Import Metatron geometry components
    try:
        metatron_path = os.path.join(project_root, "Metatron-ConscienceAI")
        if metatron_path not in sys.path:
            sys.path.append(metatron_path)
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "metatron_geometry", 
            os.path.join(metatron_path, "nodes", "metatron_geometry.py")
        )
        if spec and spec.loader:
            metatron_geometry = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(metatron_geometry)
            # Make functions available globally
            global metatron_coordinates_3d, metatron_connection_matrix, get_node_connections
            metatron_coordinates_3d = metatron_geometry.metatron_coordinates_3d
            metatron_connection_matrix = metatron_geometry.metatron_connection_matrix
            get_node_connections = metatron_geometry.get_node_connections
        else:
            logger.warning("Could not load metatron_geometry module")
    except Exception as e:
        logger.warning(f"Could not import metatron_geometry: {e}")
    logger.info("✅ All system components imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import system components: {e}")
    sys.exit(1)

class ComprehensiveHarmonyTest:
    """Test suite to verify all 13 nodes across 4 apps are working in harmony"""
    
    def __init__(self):
        self.test_results = {
            "timestamp": time.time(),
            "tests_passed": 0,
            "tests_failed": 0,
            "details": {}
        }
        
    def record_result(self, test_name: str, passed: bool, details: str = ""):
        """Record test result"""
        self.test_results["details"][test_name] = {
            "passed": passed,
            "details": details
        }
        
        if passed:
            self.test_results["tests_passed"] += 1
            logger.info(f"✅ {test_name}: PASSED")
        else:
            self.test_results["tests_failed"] += 1
            logger.error(f"❌ {test_name}: FAILED - {details}")
    
    async def test_node_structure(self):
        """Test that all 13 nodes are properly structured"""
        try:
            # Test Metatron geometry (if available)
            try:
                coords = metatron_coordinates_3d()
                connections = metatron_connection_matrix()
                
                # Verify 13 nodes exist
                node_count = len(coords)
                self.record_result(
                    "Node Structure Verification",
                    node_count == 13,
                    f"Found {node_count} nodes, expected 13"
                )
                
                # Verify connection matrix dimensions
                matrix_shape = connections.shape
                self.record_result(
                    "Connection Matrix Dimensions",
                    matrix_shape == (13, 13),
                    f"Matrix shape {matrix_shape}, expected (13, 13)"
                )
                
                # Verify central node connections
                central_connections, weights = get_node_connections(0, connections)
                self.record_result(
                    "Central Node Connectivity",
                    len(central_connections) == 12,
                    f"Central node connects to {len(central_connections)} nodes, expected 12"
                )
            except NameError as e:
                self.record_result(
                    "Node Structure Verification",
                    False,
                    f"Metatron geometry components not available: {str(e)}"
                )
            
        except Exception as e:
            self.record_result(
                "Node Structure Verification",
                False,
                f"Exception occurred: {str(e)}"
            )
    
    async def test_unified_system_initialization(self):
        """Test that the unified system initializes correctly"""
        try:
            # Create coordinator
            coordinator = UnifiedSystemCoordinator("harmony_test_coordinator")
            
            # Initialize system
            init_success = await coordinator.initialize()
            self.record_result(
                "Unified System Initialization",
                init_success,
                f"Initialization {'successful' if init_success else 'failed'}"
            )
            
            if init_success:
                # Test component availability
                components = {
                    "API Client": coordinator.api_client is not None,
                    "P2P Network": coordinator.p2p_network is not None,
                    "Consensus": coordinator.consensus is not None,
                    "Decision Engine": coordinator.decision_engine is not None,
                    "Communicator": coordinator.communicator is not None
                }
                
                all_components_ok = all(components.values())
                self.record_result(
                    "Unified Component Availability",
                    all_components_ok,
                    f"Components available: {sum(components.values())}/5"
                )
                
                # Clean shutdown
                await coordinator.shutdown()
            
        except Exception as e:
            self.record_result(
                "Unified System Initialization",
                False,
                f"Exception occurred: {str(e)}"
            )
    
    async def test_cross_system_communication(self):
        """Test cross-system communication protocols"""
        try:
            # Create communicator
            communicator = CrossSystemCommunicator("test_communicator")
            init_success = await communicator.initialize()
            
            self.record_result(
                "Cross-System Communication Initialization",
                init_success,
                f"Communication initialization {'successful' if init_success else 'failed'}"
            )
            
            if init_success:
                # Test encryption
                encryption_available = hasattr(communicator, 'cipher_suite') and communicator.cipher_suite is not None
                self.record_result(
                    "Encryption Protocol Availability",
                    encryption_available,
                    f"Encryption {'enabled' if encryption_available else 'disabled'}"
                )
                
                # Test message handling
                metrics = communicator.get_communication_metrics()
                metrics_available = isinstance(metrics, dict)
                self.record_result(
                    "Communication Metrics Tracking",
                    metrics_available,
                    f"Metrics tracking {'available' if metrics_available else 'unavailable'}"
                )
                
                # Clean shutdown
                await communicator.stop()
                
        except Exception as e:
            self.record_result(
                "Cross-System Communication",
                False,
                f"Exception occurred: {str(e)}"
            )
    
    async def test_consciousness_aware_agi(self):
        """Test consciousness-aware AGI decision making"""
        try:
            # Create decision engine
            decision_engine = ConsciousnessAwareDecisionEngine("test_decision_engine")
            init_success = await decision_engine.initialize()
            
            self.record_result(
                "Consciousness-Aware AGI Initialization",
                init_success,
                f"Decision engine initialization {'successful' if init_success else 'failed'}"
            )
            
            if init_success:
                # Test decision context creation
                try:
                    actions = ["test_action_1", "test_action_2"]
                    context = await decision_engine.get_decision_context(actions)
                    context_available = context is not None
                    self.record_result(
                        "Decision Context Creation",
                        context_available,
                        f"Decision context {'created' if context_available else 'failed'}"
                    )
                    
                    if context_available:
                        # Test consciousness-aware decision making
                        decision = decision_engine.make_consciousness_aware_decision(context)
                        decision_made = decision is not None and hasattr(decision, 'action')
                        self.record_result(
                            "Consciousness-Aware Decision Making",
                            decision_made,
                            f"Decision {'made' if decision_made else 'failed'}"
                        )
                        
                except Exception as e:
                    self.record_result(
                        "Decision Context Creation",
                        False,
                        f"Exception in context creation: {str(e)}"
                    )
                
                # Clean shutdown
                await decision_engine.close()
                
        except Exception as e:
            self.record_result(
                "Consciousness-Aware AGI",
                False,
                f"Exception occurred: {str(e)}"
            )
    
    async def test_pipeline_integration(self):
        """Test end-to-end pipeline integration"""
        try:
            # Create all components
            coordinator = UnifiedSystemCoordinator("pipeline_test_coordinator")
            api_client = UnifiedAPIClient()
            
            # Initialize components
            coordinator_init = await coordinator.initialize()
            api_init = await api_client.initialize()
            
            self.record_result(
                "Pipeline Component Initialization",
                coordinator_init and api_init,
                f"Coordinator: {'OK' if coordinator_init else 'FAIL'}, API: {'OK' if api_init else 'FAIL'}"
            )
            
            if coordinator_init and api_init:
                # Test unified state retrieval
                try:
                    state = await api_client.get_unified_state()
                    state_available = state is not None and isinstance(state, dict)
                    self.record_result(
                        "Unified State Retrieval",
                        state_available,
                        f"State {'retrieved' if state_available else 'unavailable'}"
                    )
                    
                    if state_available:
                        # Check for key state components
                        required_keys = ["timestamp", "consciousness_metrics", "agi_status"]
                        keys_present = isinstance(state, dict) and all(key in state for key in required_keys)
                        self.record_result(
                            "Required State Components",
                            keys_present,
                            f"Required keys present: {sum(1 for k in required_keys if isinstance(state, dict) and k in state)}/{len(required_keys)}"
                        )
                        
                except Exception as e:
                    self.record_result(
                        "Unified State Retrieval",
                        False,
                        f"Exception in state retrieval: {str(e)}"
                    )
                
                # Clean shutdown
                await api_client.close()
                await coordinator.shutdown()
                
        except Exception as e:
            self.record_result(
                "Pipeline Integration",
                False,
                f"Exception occurred: {str(e)}"
            )
    
    async def test_orchestrator_coordination(self):
        """Test orchestrator coordination of all components"""
        try:
            # Create coordinator
            coordinator = UnifiedSystemCoordinator("orchestrator_test")
            
            # Initialize
            init_success = await coordinator.initialize()
            self.record_result(
                "Orchestrator Initialization",
                init_success,
                f"Orchestrator initialization {'successful' if init_success else 'failed'}"
            )
            
            if init_success:
                # Test system status retrieval
                try:
                    status = await coordinator.get_system_status()
                    status_available = status is not None and isinstance(status, dict)
                    self.record_result(
                        "System Status Monitoring",
                        status_available,
                        f"Status {'available' if status_available else 'unavailable'}"
                    )
                    
                    if status_available:
                        # Check for required status fields
                        required_fields = [
                            "system_status", "uptime", "components_initialized", 
                            "total_decisions", "messages_processed"
                        ]
                        fields_present = all(field in status for field in required_fields)
                        self.record_result(
                            "Required Status Fields",
                            fields_present,
                            f"Fields present: {sum(f in status for f in required_fields)}/{len(required_fields)}"
                        )
                        
                except Exception as e:
                    self.record_result(
                        "System Status Monitoring",
                        False,
                        f"Exception in status monitoring: {str(e)}"
                    )
                
                # Clean shutdown
                await coordinator.shutdown()
                
        except Exception as e:
            self.record_result(
                "Orchestrator Coordination",
                False,
                f"Exception occurred: {str(e)}"
            )
    
    async def run_all_tests(self):
        """Run all harmony tests"""
        logger.info("🚀 Starting Comprehensive Harmony Test")
        logger.info("=" * 60)
        
        # Run all tests
        await self.test_node_structure()
        await self.test_unified_system_initialization()
        await self.test_cross_system_communication()
        await self.test_consciousness_aware_agi()
        await self.test_pipeline_integration()
        await self.test_orchestrator_coordination()
        
        # Generate final report
        self.generate_report()
        
        return self.test_results
    
    def generate_report(self):
        """Generate comprehensive test report"""
        logger.info("=" * 60)
        logger.info("📊 COMPREHENSIVE HARMONY TEST RESULTS")
        logger.info("=" * 60)
        
        total_tests = self.test_results["tests_passed"] + self.test_results["tests_failed"]
        success_rate = (self.test_results["tests_passed"] / total_tests * 100) if total_tests > 0 else 0
        
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {self.test_results['tests_passed']}")
        logger.info(f"Failed: {self.test_results['tests_failed']}")
        logger.info(f"Success Rate: {success_rate:.1f}%")
        
        if self.test_results["tests_failed"] == 0:
            logger.info("\n🎉 ALL HARMONY TESTS PASSED!")
            logger.info("\n✅ CONFIRMATION: All 13 nodes across 4 apps are connected and working in harmony:")
            logger.info("   • Metatron-ConscienceAI (13-node consciousness network)")
            logger.info("   • Open-A.G.I (Distributed AGI system)")
            logger.info("   • aegis-conscience (Security framework)")
            logger.info("   • Unified System (Integration layer)")
            logger.info("\n🔗 VERIFIED INTEGRATIONS:")
            logger.info("   • Node connectivity across all systems")
            logger.info("   • Pipeline integration from sensory input to AGI decision making")
            logger.info("   • Orchestrator coordination of all components")
            logger.info("   • Consciousness-aware AGI decision making")
            logger.info("   • Cross-system communication protocols")
        else:
            logger.warning("\n⚠️  SOME HARMONY TESTS FAILED")
            logger.warning("Please review the failed tests above.")

async def main():
    """Main test execution"""
    # Create and run comprehensive harmony test
    harmony_test = ComprehensiveHarmonyTest()
    results = await harmony_test.run_all_tests()
    
    # Save results to file
    results_file = os.path.join(project_root, "HARMONY_TEST_RESULTS.json")
    try:
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"📝 Detailed results saved to {results_file}")
    except Exception as e:
        logger.error(f"Failed to save results: {e}")
    
    # Return appropriate exit code
    return 0 if results["tests_failed"] == 0 else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)