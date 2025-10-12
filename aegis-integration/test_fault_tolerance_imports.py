"""
Test script to verify that fault_tolerance_sacred.py imports work correctly
"""

import sys
import os

# Add the aegis-conscience path to sys.path
aegis_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'aegis-conscience')
if os.path.exists(aegis_path):
    if aegis_path not in sys.path:
        sys.path.insert(0, aegis_path)

# Import the fault tolerance module
import fault_tolerance_sacred

def test_imports():
    """Test that all required classes are imported correctly"""
    print("Testing fault_tolerance_sacred imports...")
    
    # Check that the classes are not None
    assert fault_tolerance_sacred.AEGIS_P2PNetwork is not None, "AEGIS_P2PNetwork should not be None"
    assert fault_tolerance_sacred.AEGIS_PBFTConsensus is not None, "AEGIS_PBFTConsensus should not be None"
    assert fault_tolerance_sacred.AEGIS_CryptoManager is not None, "AEGIS_CryptoManager should not be None"
    
    # Check that the aliases work
    assert fault_tolerance_sacred.P2PNetwork is not None, "P2PNetwork alias should not be None"
    assert fault_tolerance_sacred.PBFTConsensus is not None, "PBFTConsensus alias should not be None"
    assert fault_tolerance_sacred.CryptoManager is not None, "CryptoManager alias should not be None"
    
    print("All imports successful!")
    print(f"AEGIS_P2PNetwork: {fault_tolerance_sacred.AEGIS_P2PNetwork}")
    print(f"AEGIS_PBFTConsensus: {fault_tolerance_sacred.AEGIS_PBFTConsensus}")
    print(f"AEGIS_CryptoManager: {fault_tolerance_sacred.AEGIS_CryptoManager}")
    
    # Try to instantiate the classes
    try:
        p2p = fault_tolerance_sacred.P2PNetwork()
        print("P2PNetwork instantiation successful")
    except Exception as e:
        print(f"P2PNetwork instantiation failed: {e}")
    
    try:
        crypto = fault_tolerance_sacred.CryptoManager("test_node")
        print("CryptoManager instantiation successful")
    except Exception as e:
        print(f"CryptoManager instantiation failed: {e}")
    
    try:
        pbft = fault_tolerance_sacred.PBFTConsensus("test_node", None)
        print("PBFTConsensus instantiation successful")
    except Exception as e:
        print(f"PBFTConsensus instantiation failed: {e}")

if __name__ == "__main__":
    test_imports()