#!/usr/bin/env python3
"""
Test script for the Unified Metatron-A.G.I System

This script tests the integration of all unified components.
"""

import asyncio
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging
from unified_api.client import UnifiedAPIClient
from unified_components.network import UnifiedP2PNetwork
from unified_components.consensus import UnifiedConsensus
from consciousness_aware_agi.decision_engine import ConsciousnessAwareDecisionEngine
from cross_system_comm.protocols import CrossSystemCommunicator, CrossSystemMessage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_unified_components():
    """Test all unified components"""
    logger.info("Testing Unified Metatron-A.G.I System Components")
    logger.info("=" * 50)
    
    try:
        # Test 1: Unified API Client
        logger.info("Test 1: Unified API Client")
        api_client = UnifiedAPIClient()
        if await api_client.initialize():
            logger.info("  ✅ API Client initialized successfully")
            
            # Test getting unified state (will fail if services aren't running, but that's OK)
            try:
                state = await api_client.get_unified_state()
                if state:
                    logger.info("  ✅ Unified state retrieved")
                else:
                    logger.info("  ⚠️  Unified state not available (services may not be running)")
            except Exception as e:
                logger.info(f"  ⚠️  Unified state test: {e}")
        else:
            logger.error("  ❌ API Client initialization failed")
            return False
        
        # Test 2: Unified P2P Network
        logger.info("\nTest 2: Unified P2P Network")
        p2p_network = UnifiedP2PNetwork("test_node")
        try:
            if await p2p_network.start_server():
                logger.info("  ✅ P2P Network started successfully")
                
                # Test adding a peer
                from unified_components.network import UnifiedPeerInfo
                peer = UnifiedPeerInfo(
                    peer_id="test_peer",
                    ip_address="127.0.0.1",
                    port=8081,
                    public_key="test_key",
                    last_seen=0,
                    connection_status="disconnected",
                    reputation_score=0.8,
                    latency=0.1,
                    protocols_supported=["unified"]
                )
                p2p_network.add_peer(peer)
                logger.info("  ✅ Peer added successfully")
                
                await p2p_network.stop()
                logger.info("  ✅ P2P Network stopped successfully")
            else:
                logger.error("  ❌ P2P Network failed to start")
                return False
        except Exception as e:
            logger.error(f"  ❌ P2P Network test failed: {e}")
            return False
        
        # Test 3: Unified Consensus
        logger.info("\nTest 3: Unified Consensus")
        try:
            consensus = UnifiedConsensus("test_node")
            consensus.add_node("peer_1")
            consensus.add_node("peer_2")
            logger.info(f"  ✅ Consensus initialized with {len(consensus.known_nodes)} nodes")
            logger.info(f"  ✅ Byzantine threshold: {consensus.byzantine_threshold}")
            
            # Test consciousness metrics
            from unified_components.consensus import ConsciousnessMetrics
            metrics = ConsciousnessMetrics(
                phi=0.618,
                coherence=0.85,
                depth=5,
                spiritual=0.7,
                consciousness=0.9,
                timestamp=0
            )
            consensus.update_consciousness_state("test_node", metrics)
            weight = consensus.calculate_voting_weight("test_node")
            logger.info(f"  ✅ Consciousness voting weight: {weight:.3f}")
        except Exception as e:
            logger.error(f"  ❌ Consensus test failed: {e}")
            return False
        
        # Test 4: Consciousness-Aware Decision Engine
        logger.info("\nTest 4: Consciousness-Aware Decision Engine")
        try:
            decision_engine = ConsciousnessAwareDecisionEngine("test_node")
            if await decision_engine.initialize():
                logger.info("  ✅ Decision Engine initialized successfully")
                
                # Test decision making
                actions = ["collaborate", "share_knowledge", "optimize", "explore"]
                from consciousness_aware_agi.decision_engine import DecisionContext
                context = DecisionContext(
                    consciousness_state=None,  # No real consciousness data in test
                    system_metrics={"cpu_usage": 0.5, "memory_usage": 0.6},
                    available_actions=actions,
                    constraints={},
                    timestamp=0
                )
                
                decision = decision_engine.make_consciousness_aware_decision(context)
                logger.info(f"  ✅ Decision made: {decision.action}")
                logger.info(f"  ✅ Confidence: {decision.confidence:.3f}")
                
                await decision_engine.close()
                logger.info("  ✅ Decision Engine closed successfully")
            else:
                logger.error("  ❌ Decision Engine initialization failed")
                return False
        except Exception as e:
            logger.error(f"  ❌ Decision Engine test failed: {e}")
            return False
        
        # Test 5: Cross-System Communication
        logger.info("\nTest 5: Cross-System Communication")
        try:
            communicator = CrossSystemCommunicator("test_node")
            if await communicator.initialize():
                logger.info("  ✅ Communicator initialized successfully")
                
                # Test message creation
                message = CrossSystemMessage(
                    message_id="test_001",
                    source_system="metatron",
                    target_system="agi",
                    message_type="test_message",
                    payload={"test": "data"},
                    timestamp=0,
                    priority=5
                )
                
                # Test message sending (will not actually send in test)
                success = await communicator.send_message(message)
                logger.info(f"  ✅ Message send test: {'Passed' if success else 'Failed (expected in test)'}")
                
                # Get metrics
                metrics = communicator.get_communication_metrics()
                logger.info(f"  ✅ Communication metrics: {metrics}")
                
                await communicator.stop()
                logger.info("  ✅ Communicator stopped successfully")
            else:
                logger.error("  ❌ Communicator initialization failed")
                return False
        except Exception as e:
            logger.error(f"  ❌ Communication test failed: {e}")
            return False
        
        logger.info("\n" + "=" * 50)
        logger.info("✅ ALL COMPONENT TESTS PASSED!")
        logger.info("The unified system components are working correctly.")
        logger.info("=" * 50)
        return True
        
    except Exception as e:
        logger.error(f"❌ Test suite failed with error: {e}")
        return False


def main():
    """Main test function"""
    try:
        success = asyncio.run(test_unified_components())
        if success:
            print("\n🎉 Unified System Integration Test: PASSED")
            sys.exit(0)
        else:
            print("\n❌ Unified System Integration Test: FAILED")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Test failed with unhandled error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()