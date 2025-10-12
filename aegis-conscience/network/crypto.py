"""
Cryptographic Framework for AEGIS-Conscience Network
Based on Ed25519 signatures and X25519 encryption
"""

import os
import time
import json
import hashlib
import secrets
from typing import Dict, Optional, Tuple, Any
from dataclasses import dataclass, asdict

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, x25519
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidSignature

from schemas import ConsciousnessState


@dataclass
class NodeIdentity:
    """Node cryptographic identity"""
    node_id: str
    signing_key: Optional[ed25519.Ed25519PrivateKey]
    encryption_key: Optional[x25519.X25519PrivateKey]
    public_signing_key: ed25519.Ed25519PublicKey
    public_encryption_key: x25519.X25519PublicKey
    
    def __post_init__(self):
        """Derive public keys if not provided"""
        if not hasattr(self, 'public_signing_key') or self.public_signing_key is None:
            if self.signing_key:
                self.public_signing_key = self.signing_key.public_key()
        if not hasattr(self, 'public_encryption_key') or self.public_encryption_key is None:
            if self.encryption_key:
                self.public_encryption_key = self.encryption_key.public_key()


class CryptoManager:
    """Manages cryptographic operations for the network"""
    
    def __init__(self, node_id: str = ""):
        self.node_id = node_id or secrets.token_hex(16)
        self.identity: Optional[NodeIdentity] = None
        self.peer_identities: Dict[str, NodeIdentity] = {}
        self.key_file = f"node_{self.node_id}.key.enc"
        
    def generate_or_load_identity(self, password: Optional[str] = None) -> bool:
        """
        Generate a new identity or load existing one from encrypted storage
        
        Args:
            password: Password to decrypt existing key file (if exists)
            
        Returns:
            bool: True if successful
        """
        if os.path.exists(self.key_file) and password:
            # Try to load existing identity
            return self._load_identity(password)
        else:
            # Generate new identity
            return self._generate_new_identity(password)
    
    def _generate_new_identity(self, password: Optional[str] = None) -> bool:
        """Generate a new cryptographic identity for this node"""
        try:
            signing_key = ed25519.Ed25519PrivateKey.generate()
            encryption_key = x25519.X25519PrivateKey.generate()
            
            self.identity = NodeIdentity(
                node_id=self.node_id,
                signing_key=signing_key,
                encryption_key=encryption_key,
                public_signing_key=signing_key.public_key(),
                public_encryption_key=encryption_key.public_key()
            )
            
            # Save encrypted key if password provided
            if password:
                self._save_identity(password)
                
            return True
        except Exception as e:
            print(f"Error generating identity: {e}")
            return False
    
    def _save_identity(self, password: str) -> bool:
        """Save identity to encrypted file"""
        try:
            if not self.identity or not self.identity.signing_key or not self.identity.encryption_key:
                return False
                
            # Serialize private keys
            signing_key_bytes = self.identity.signing_key.private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption()
            )
            
            encryption_key_bytes = self.identity.encryption_key.private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption()
            )
            
            # Create data to encrypt
            key_data = {
                "signing_key": signing_key_bytes.hex(),
                "encryption_key": encryption_key_bytes.hex(),
                "node_id": self.node_id
            }
            
            # Derive encryption key from password
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = kdf.derive(password.encode())
            
            # Encrypt with ChaCha20-Poly1305
            chacha = ChaCha20Poly1305(key)
            nonce = os.urandom(12)
            plaintext = json.dumps(key_data).encode()
            ciphertext = chacha.encrypt(nonce, plaintext, None)
            
            # Save to file (salt + nonce + ciphertext)
            with open(self.key_file, 'wb') as f:
                f.write(salt + nonce + ciphertext)
                
            print(f"Identity saved to {self.key_file}")
            return True
        except Exception as e:
            print(f"Error saving identity: {e}")
            return False
    
    def _load_identity(self, password: str) -> bool:
        """Load identity from encrypted file"""
        try:
            # Read encrypted file
            with open(self.key_file, 'rb') as f:
                data = f.read()
            
            if len(data) < 28:  # 16 (salt) + 12 (nonce) = 28
                print("Invalid key file")
                return False
                
            # Extract components
            salt = data[:16]
            nonce = data[16:28]
            ciphertext = data[28:]
            
            # Derive encryption key from password
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = kdf.derive(password.encode())
            
            # Decrypt
            chacha = ChaCha20Poly1305(key)
            plaintext = chacha.decrypt(nonce, ciphertext, None)
            key_data = json.loads(plaintext.decode())
            
            # Recreate keys
            signing_key_bytes = bytes.fromhex(key_data["signing_key"])
            encryption_key_bytes = bytes.fromhex(key_data["encryption_key"])
            
            signing_key = ed25519.Ed25519PrivateKey.from_private_bytes(signing_key_bytes)
            encryption_key = x25519.X25519PrivateKey.from_private_bytes(encryption_key_bytes)
            
            self.identity = NodeIdentity(
                node_id=key_data["node_id"],
                signing_key=signing_key,
                encryption_key=encryption_key,
                public_signing_key=signing_key.public_key(),
                public_encryption_key=encryption_key.public_key()
            )
            
            print(f"Identity loaded from {self.key_file}")
            return True
        except Exception as e:
            print(f"Error loading identity: {e}")
            return False
    
    def sign_state(self, state: ConsciousnessState) -> bytes:
        """
        Sign a consciousness state with this node's private key
        
        Args:
            state: ConsciousnessState to sign
            
        Returns:
            bytes: Signature
        """
        if not self.identity or not self.identity.signing_key:
            raise ValueError("Identity not initialized")
            
        # Serialize state for signing
        state_data = self._serialize_state_for_signing(state)
        return self.identity.signing_key.sign(state_data)
    
    def verify_state(self, state: ConsciousnessState, signature: bytes, 
                     peer_public_key: bytes) -> bool:
        """
        Verify a signed consciousness state
        
        Args:
            state: ConsciousnessState to verify
            signature: Signature bytes
            peer_public_key: Peer's public key bytes
            
        Returns:
            bool: True if signature is valid
        """
        try:
            # Deserialize peer's public key
            public_key = ed25519.Ed25519PublicKey.from_public_bytes(peer_public_key)
            
            # Serialize state for verification
            state_data = self._serialize_state_for_signing(state)
            
            # Verify signature
            public_key.verify(signature, state_data)
            return True
        except InvalidSignature:
            return False
        except Exception:
            return False
    
    def _serialize_state_for_signing(self, state: ConsciousnessState) -> bytes:
        """
        Serialize a consciousness state for signing/verification
        
        Args:
            state: ConsciousnessState to serialize
            
        Returns:
            bytes: Serialized state
        """
        # Create a dictionary without the signature field
        state_dict = {
            'node_id': state.node_id,
            'timestamp': state.timestamp,
            'entropy': state.entropy,
            'valence': state.valence,
            'arousal': state.arousal,
            'coherence': state.coherence,
            'empathy_score': state.empathy_score,
            'insight_strength': state.insight_strength
        }
        
        # Sort keys for consistent serialization
        state_json = json.dumps(state_dict, sort_keys=True)
        return state_json.encode()
    
    def encrypt_message(self, message: bytes, peer_public_key: bytes) -> bytes:
        """
        Encrypt a message for a peer using their public key
        
        Args:
            message: Message to encrypt
            peer_public_key: Peer's public encryption key
            
        Returns:
            bytes: Encrypted message
        """
        try:
            if not self.identity or not self.identity.encryption_key:
                raise ValueError("Identity not initialized")
                
            # Deserialize peer's public key
            peer_key = x25519.X25519PublicKey.from_public_bytes(peer_public_key)
            
            # Perform key exchange
            shared_key = self.identity.encryption_key.exchange(peer_key)
            
            # Derive encryption key using HKDF
            derived_key = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=None,
                info=b"aegis-conscience-encryption"
            ).derive(shared_key)
            
            # Encrypt with ChaCha20-Poly1305
            chacha = ChaCha20Poly1305(derived_key)
            nonce = os.urandom(12)
            ciphertext = chacha.encrypt(nonce, message, None)
            
            # Return nonce + ciphertext
            return nonce + ciphertext
        except Exception as e:
            raise Exception(f"Encryption failed: {e}")
    
    def decrypt_message(self, encrypted_message: bytes, sender_public_key: bytes) -> bytes:
        """
        Decrypt a message using this node's private key
        
        Args:
            encrypted_message: Encrypted message (nonce + ciphertext)
            sender_public_key: Sender's public key for key exchange
            
        Returns:
            bytes: Decrypted message
        """
        try:
            if not self.identity or not self.identity.encryption_key:
                raise ValueError("Identity not initialized")
                
            # Extract nonce and ciphertext
            nonce = encrypted_message[:12]
            ciphertext = encrypted_message[12:]
            
            # Deserialize sender's public key
            sender_key = x25519.X25519PublicKey.from_public_bytes(sender_public_key)
            
            # Perform key exchange
            shared_key = self.identity.encryption_key.exchange(sender_key)
            
            # Derive encryption key using HKDF
            derived_key = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=None,
                info=b"aegis-conscience-encryption"
            ).derive(shared_key)
            
            # Decrypt with ChaCha20-Poly1305
            chacha = ChaCha20Poly1305(derived_key)
            plaintext = chacha.decrypt(nonce, ciphertext, None)
            
            return plaintext
        except Exception as e:
            raise Exception(f"Decryption failed: {e}")
    
    def get_public_keys(self) -> Tuple[bytes, bytes]:
        """
        Get this node's public keys
        
        Returns:
            Tuple[bytes, bytes]: (signing_public_key, encryption_public_key)
        """
        if not self.identity:
            raise ValueError("Identity not initialized")
            
        signing_pub = self.identity.public_signing_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        encryption_pub = self.identity.public_encryption_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        return signing_pub, encryption_pub
    
    def add_peer_identity(self, peer_id: str, signing_pub_key: bytes, 
                         encryption_pub_key: bytes) -> None:
        """
        Add a peer's identity to the known identities
        
        Args:
            peer_id: Peer's node ID
            signing_pub_key: Peer's signing public key
            encryption_pub_key: Peer's encryption public key
        """
        signing_key = ed25519.Ed25519PublicKey.from_public_bytes(signing_pub_key)
        encryption_key = x25519.X25519PublicKey.from_public_bytes(encryption_pub_key)
        
        self.peer_identities[peer_id] = NodeIdentity(
            node_id=peer_id,
            signing_key=None,  # We don't have their private keys
            encryption_key=None,
            public_signing_key=signing_key,
            public_encryption_key=encryption_key
        )


# Example usage
if __name__ == "__main__":
    # Create crypto manager
    crypto = CryptoManager("test_node_1")
    
    # Generate new identity with password
    password = "test_password_123"
    if crypto.generate_or_load_identity(password):
        print("Identity generated and saved successfully")
        
        # Get public keys
        signing_pub, encryption_pub = crypto.get_public_keys()
        print(f"Signing public key: {signing_pub.hex()[:32]}...")
        print(f"Encryption public key: {encryption_pub.hex()[:32]}...")
        
        # Create a test state
        state = ConsciousnessState(
            node_id="test_node_1",
            timestamp=time.time(),
            entropy=0.5,
            valence=0.3,
            arousal=0.7,
            coherence=0.8,
            empathy_score=0.6,
            insight_strength=0.4
        )
        
        # Sign the state
        signature = crypto.sign_state(state)
        print(f"Signature: {signature.hex()[:32]}...")
        
        # Verify the signature
        is_valid = crypto.verify_state(state, signature, signing_pub)
        print(f"Signature valid: {is_valid}")
        
        # Test loading identity
        crypto2 = CryptoManager("test_node_1")
        if crypto2.generate_or_load_identity(password):
            print("Identity loaded successfully")
        else:
            print("Failed to load identity")