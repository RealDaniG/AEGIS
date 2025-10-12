"""
Verify that the actual AEGIS classes are being imported rather than fallbacks
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

def verify_aegis_imports():
    """Verify that actual AEGIS classes are imported"""
    print("Verifying AEGIS imports...")
    
    # Check that we're not using fallback classes
    is_p2p_fallback = fault_tolerance_sacred.AEGIS_P2PNetwork.__name__ == 'FallbackP2PNetwork'
    is_pbft_fallback = fault_tolerance_sacred.AEGIS_PBFTConsensus.__name__ == 'FallbackPBFTConsensus'
    is_crypto_fallback = fault_tolerance_sacred.AEGIS_CryptoManager.__name__ == 'FallbackCryptoManager'
    
    print(f"Using fallback P2PNetwork: {is_p2p_fallback}")
    print(f"Using fallback PBFTConsensus: {is_pbft_fallback}")
    print(f"Using fallback CryptoManager: {is_crypto_fallback}")
    
    # Show the actual class names
    print(f"AEGIS_P2PNetwork class: {fault_tolerance_sacred.AEGIS_P2PNetwork}")
    print(f"AEGIS_PBFTConsensus class: {fault_tolerance_sacred.AEGIS_PBFTConsensus}")
    print(f"AEGIS_CryptoManager class: {fault_tolerance_sacred.AEGIS_CryptoManager}")
    
    if not (is_p2p_fallback or is_pbft_fallback or is_crypto_fallback):
        print("SUCCESS: All AEGIS classes imported successfully!")
    else:
        print("WARNING: Some fallback classes are being used")

if __name__ == "__main__":
    verify_aegis_imports()