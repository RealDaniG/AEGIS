"""
Distributed Knowledge Base for AEGIS-Conscience Network
Content-addressed storage using BLAKE3 hashing
"""

import json
import time
import hashlib
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from schemas import ConsciousnessState


@dataclass
class KnowledgeEntry:
    """Entry in the distributed knowledge base"""
    cid: str  # Content Identifier (BLAKE3 hash)
    data: Dict[str, Any]
    timestamp: float
    node_id: str
    signature: Optional[str] = None  # Store as hex string for JSON serialization
    references: List[str] = field(default_factory=list)


class KnowledgeBase:
    """Distributed knowledge base with content-addressed storage"""
    
    def __init__(self, node_id: str, storage_path: str = "./knowledge"):
        self.node_id = node_id
        self.storage_path = storage_path
        self.entries: Dict[str, KnowledgeEntry] = {}
        self.max_entries = 1000  # Limit to last 1000 states per node
        
        # Create storage directory
        os.makedirs(storage_path, exist_ok=True)
        
        # Load existing entries
        self._load_entries()
    
    def _generate_cid(self, data: Dict[str, Any]) -> str:
        """
        Generate Content Identifier (CID) using BLAKE3 hashing
        
        Args:
            data: Data to hash
            
        Returns:
            str: BLAKE3 hash as hex string
        """
        # Sort keys for consistent hashing
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.blake2b(data_str.encode(), digest_size=16).hexdigest()
    
    def store_consciousness_state(self, state: ConsciousnessState) -> str:
        """
        Store consciousness state in knowledge base
        
        Args:
            state: Consciousness state to store
            
        Returns:
            str: Content Identifier (CID) of stored entry
        """
        # Convert state to dictionary, handling bytes signature
        state_dict = {
            'node_id': state.node_id,
            'timestamp': state.timestamp,
            'entropy': state.entropy,
            'valence': state.valence,
            'arousal': state.arousal,
            'coherence': state.coherence,
            'empathy_score': state.empathy_score,
            'insight_strength': state.insight_strength,
            'signature': state.signature.hex() if state.signature else None
        }
        
        # Generate CID
        cid = self._generate_cid(state_dict)
        
        # Create knowledge entry
        entry = KnowledgeEntry(
            cid=cid,
            data=state_dict,
            timestamp=time.time(),
            node_id=self.node_id
        )
        
        # Store entry
        self.entries[cid] = entry
        
        # Save to disk
        self._save_entry(entry)
        
        # Limit entries
        self._limit_entries()
        
        print(f"Stored consciousness state with CID: {cid}")
        return cid
    
    def retrieve_entry(self, cid: str) -> Optional[KnowledgeEntry]:
        """
        Retrieve entry by Content Identifier
        
        Args:
            cid: Content Identifier
            
        Returns:
            KnowledgeEntry: Entry if found, None otherwise
        """
        # Check memory cache first
        if cid in self.entries:
            return self.entries[cid]
        
        # Try to load from disk
        entry = self._load_entry(cid)
        if entry:
            self.entries[cid] = entry
            return entry
        
        return None
    
    def sync_with_peer(self, peer_cid: str, peer_data: Dict[str, Any]) -> bool:
        """
        Sync entry from peer node
        
        Args:
            peer_cid: CID from peer
            peer_data: Data from peer
            
        Returns:
            bool: True if synced successfully
        """
        # Verify CID matches data
        calculated_cid = self._generate_cid(peer_data)
        if calculated_cid != peer_cid:
            print(f"CID mismatch: expected {peer_cid}, got {calculated_cid}")
            return False
        
        # Check if we already have this entry
        if peer_cid in self.entries:
            print(f"Entry {peer_cid} already exists")
            return True
        
        # Create and store entry
        entry = KnowledgeEntry(
            cid=peer_cid,
            data=peer_data,
            timestamp=time.time(),
            node_id=peer_data.get('node_id', 'unknown')
        )
        
        self.entries[peer_cid] = entry
        self._save_entry(entry)
        self._limit_entries()
        
        print(f"Synced entry from peer: {peer_cid}")
        return True
    
    def gossip_new_entries(self, peer_cids: List[str]) -> List[str]:
        """
        Identify entries we have that peer doesn't for gossip sync
        
        Args:
            peer_cids: List of CIDs peer has
            
        Returns:
            List[str]: List of CIDs we have but peer doesn't
        """
        peer_cid_set = set(peer_cids)
        our_cids = set(self.entries.keys())
        missing_cids = list(our_cids - peer_cid_set)
        return missing_cids
    
    def get_recent_entries(self, limit: int = 10) -> List[KnowledgeEntry]:
        """
        Get most recent entries
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List[KnowledgeEntry]: Recent entries
        """
        sorted_entries = sorted(
            self.entries.values(), 
            key=lambda x: x.timestamp, 
            reverse=True
        )
        return sorted_entries[:limit]
    
    def _save_entry(self, entry: KnowledgeEntry):
        """
        Save entry to disk
        
        Args:
            entry: Entry to save
        """
        try:
            # Convert entry to dictionary, handling bytes signature
            entry_dict = {
                'cid': entry.cid,
                'data': entry.data,
                'timestamp': entry.timestamp,
                'node_id': entry.node_id,
                'signature': entry.signature if isinstance(entry.signature, str) else (entry.signature.hex() if entry.signature else None),
                'references': entry.references
            }
            
            filename = os.path.join(self.storage_path, f"{entry.cid}.json")
            with open(filename, 'w') as f:
                json.dump(entry_dict, f, indent=2)
        except Exception as e:
            print(f"Error saving entry {entry.cid}: {e}")
    
    def _load_entry(self, cid: str) -> Optional[KnowledgeEntry]:
        """
        Load entry from disk
        
        Args:
            cid: Content Identifier
            
        Returns:
            KnowledgeEntry: Entry if found, None otherwise
        """
        try:
            filename = os.path.join(self.storage_path, f"{cid}.json")
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    data = json.load(f)
                
                # Convert references to list if it's a string
                if isinstance(data.get('references'), str):
                    data['references'] = data['references'].split(',') if data['references'] else []
                elif data.get('references') is None:
                    data['references'] = []
                
                # Convert signature from hex string if needed
                if isinstance(data.get('signature'), str):
                    data['signature'] = bytes.fromhex(data['signature'])
                
                return KnowledgeEntry(**data)
        except Exception as e:
            print(f"Error loading entry {cid}: {e}")
        
        return None
    
    def _load_entries(self):
        """Load all entries from disk"""
        try:
            for filename in os.listdir(self.storage_path):
                if filename.endswith('.json'):
                    cid = filename[:-5]  # Remove .json extension
                    entry = self._load_entry(cid)
                    if entry:
                        self.entries[cid] = entry
        except Exception as e:
            print(f"Error loading entries: {e}")
    
    def _limit_entries(self):
        """Limit number of entries to prevent unbounded growth"""
        if len(self.entries) > self.max_entries:
            # Remove oldest entries
            sorted_entries = sorted(
                self.entries.values(), 
                key=lambda x: x.timestamp
            )
            
            # Remove excess entries
            excess_count = len(self.entries) - self.max_entries
            for entry in sorted_entries[:excess_count]:
                del self.entries[entry.cid]
                
                # Remove from disk
                filename = os.path.join(self.storage_path, f"{entry.cid}.json")
                if os.path.exists(filename):
                    os.remove(filename)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get knowledge base statistics
        
        Returns:
            Dict[str, Any]: Statistics
        """
        if not self.entries:
            return {
                'total_entries': 0,
                'oldest_entry': None,
                'newest_entry': None
            }
        
        timestamps = [entry.timestamp for entry in self.entries.values()]
        return {
            'total_entries': len(self.entries),
            'oldest_entry': min(timestamps),
            'newest_entry': max(timestamps)
        }


# Example usage
if __name__ == "__main__":
    # Create knowledge base
    kb = KnowledgeBase("test_node_1")
    
    # Create test consciousness states
    state1 = ConsciousnessState(
        node_id="test_node_1",
        timestamp=time.time(),
        entropy=0.5,
        valence=0.3,
        arousal=0.7,
        coherence=0.8,
        empathy_score=0.6,
        insight_strength=0.4
    )
    
    state2 = ConsciousnessState(
        node_id="test_node_1",
        timestamp=time.time() + 10,
        entropy=0.4,
        valence=0.2,
        arousal=0.6,
        coherence=0.7,
        empathy_score=0.5,
        insight_strength=0.3
    )
    
    # Store states
    cid1 = kb.store_consciousness_state(state1)
    cid2 = kb.store_consciousness_state(state2)
    
    # Retrieve states
    entry1 = kb.retrieve_entry(cid1)
    entry2 = kb.retrieve_entry(cid2)
    
    if entry1 and entry2:
        print(f"Retrieved entries: {entry1.cid}, {entry2.cid}")
    
    # Get stats
    stats = kb.get_stats()
    print(f"Knowledge base stats: {stats}")
    
    # Test sync with peer
    peer_data = {
        'node_id': 'peer_node',
        'timestamp': time.time(),
        'entropy': 0.6,
        'valence': 0.4,
        'arousal': 0.8,
        'coherence': 0.9,
        'empathy_score': 0.7,
        'insight_strength': 0.5
    }
    
    peer_cid = kb._generate_cid(peer_data)
    kb.sync_with_peer(peer_cid, peer_data)
    
    print("Knowledge base demo completed")