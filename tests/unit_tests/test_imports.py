import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")

try:
    from schemas import ConsciousnessState
    print("[OK] Schemas imported successfully")
except Exception as e:
    print(f"✗ Error importing schemas: {e}")

try:
    from consciousness.engine import ConsciousnessEngine
    engine = ConsciousnessEngine("test_node")
    print("[OK] Consciousness engine imported and created successfully")
except Exception as e:
    print(f"✗ Error importing consciousness engine: {e}")

try:
    from network.crypto import CryptoManager
    crypto = CryptoManager("test_node")
    print("[OK] Crypto manager imported and created successfully")
    
    try:
        from consensus.pbft import PBFTConsensus
        pbft = PBFTConsensus("test_node", crypto)
        print("[OK] PBFT consensus imported and created successfully")
    except Exception as e:
        print(f"✗ Error importing PBFT consensus: {e}")
except Exception as e:
    print(f"✗ Error importing crypto manager: {e}")
    # Create a mock crypto manager for PBFT testing
    class MockCryptoManager:
        def sign_state(self, state):
            return b"mock_signature"
    
    try:
        from consensus.pbft import PBFTConsensus
        pbft = PBFTConsensus("test_node", MockCryptoManager())
        print("[OK] PBFT consensus imported and created with mock crypto successfully")
    except Exception as e:
        print(f"✗ Error importing PBFT consensus: {e}")

try:
    from network.p2p import P2PNetwork
    p2p = P2PNetwork("test_node")
    print("[OK] P2P network imported and created successfully")
except Exception as e:
    print(f"✗ Error importing P2P network: {e}")

print("Import testing complete.")