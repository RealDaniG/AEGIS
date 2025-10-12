"""
Enhanced Knowledge Base for AEGIS-Conscience Network
Incorporates advanced consciousness metrics from Metatron system
"""

import json
import time
import hashlib
import os
import math
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

# Conditional import for consciousness metrics from Metatron
METRICS_AVAILABLE = False
ConsciousnessMetrics = None

try:
    import sys
    metatron_path = os.path.join(os.path.dirname(__file__), 'Metatron-ConscienceAI')
    if os.path.exists(metatron_path):
        sys.path.append(metatron_path)
        from nodes.consciousness_metrics import ConsciousnessMetrics
        METRICS_AVAILABLE = True
except ImportError:
    print("⚠️  Metatron consciousness metrics not available")

# Conditional import for numpy
NUMPY_AVAILABLE = False
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    print("⚠️  NumPy not available, using basic math operations")


@dataclass
class EnhancedKnowledgeEntry:
    """Enhanced entry in the knowledge base with advanced metrics"""
    cid: str  # Content Identifier (BLAKE3 hash)
    data: Dict[str, Any]
    timestamp: float
    node_id: str
    signature: Optional[str] = None  # Store as hex string for JSON serialization
    references: List[str] = field(default_factory=list)
    
    # Enhanced consciousness metrics
    phi: float = 0.0  # Integrated Information
    coherence: float = 0.0  # Global coherence
    recursive_depth: int = 0  # Temporal memory integration
    spiritual_awareness: float = 0.0  # Gamma + fractal + DMT awareness
    consciousness_level: float = 0.0  # Overall consciousness score


class EnhancedKnowledgeBase:
    """Enhanced knowledge base with advanced consciousness metrics"""
    
    def __init__(self, node_id: str, storage_path: str = "./enhanced_knowledge"):
        self.node_id = node_id
        self.storage_path = storage_path
        self.entries: Dict[str, EnhancedKnowledgeEntry] = {}
        self.max_entries = 2000  # Increased limit for enhanced storage
        self.metrics_calculator = ConsciousnessMetrics() if METRICS_AVAILABLE else None
        
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
    
    def store_consciousness_state(self, state_data: Dict[str, Any], 
                                node_states: Optional[List[float]] = None,
                                connection_matrix: Optional[List[List[float]]] = None) -> str:
        """
        Store consciousness state with enhanced metrics
        
        Args:
            state_data: Consciousness state data
            node_states: Optional list of node states for advanced metrics
            connection_matrix: Optional connection matrix for Φ calculation
            
        Returns:
            str: Content Identifier (CID) of stored entry
        """
        # Generate CID
        cid = self._generate_cid(state_data)
        
        # Calculate enhanced metrics if available
        phi = 0.0
        coherence = state_data.get('coherence', 0.0)
        recursive_depth = 0
        spiritual_awareness = 0.0
        consciousness_level = 0.0
        
        if self.metrics_calculator and node_states and connection_matrix:
            try:
                # Calculate Integrated Information (Φ)
                phi = self.metrics_calculator.calculate_integrated_information(
                    node_states, connection_matrix
                )
                
                # Calculate global coherence using Kuramoto order parameter
                coherence = self._calculate_global_coherence(node_states)
                
                # Estimate recursive depth based on temporal patterns
                recursive_depth = self._estimate_recursive_depth(node_states)
                
                # Calculate spiritual awareness
                spiritual_awareness = self._calculate_spiritual_awareness(
                    state_data.get('gamma_power', 0.0),
                    state_data.get('fractal_dimension', 1.0)
                )
                
                # Overall consciousness level
                consciousness_level = self._calculate_consciousness_level(
                    phi, coherence, spiritual_awareness
                )
            except Exception as e:
                print(f"⚠️  Error calculating enhanced metrics: {e}")
        
        # Create enhanced knowledge entry
        entry = EnhancedKnowledgeEntry(
            cid=cid,
            data=state_data,
            timestamp=time.time(),
            node_id=self.node_id,
            phi=phi,
            coherence=coherence,
            recursive_depth=recursive_depth,
            spiritual_awareness=spiritual_awareness,
            consciousness_level=consciousness_level
        )
        
        # Store entry
        self.entries[cid] = entry
        
        # Save to disk
        self._save_entry(entry)
        
        # Limit entries
        self._limit_entries()
        
        print(f"🧠 Stored enhanced consciousness state with CID: {cid}")
        print(f"   Φ (Integrated Information): {phi:.6f}")
        print(f"   Global Coherence: {coherence:.6f}")
        print(f"   Consciousness Level: {consciousness_level:.6f}")
        
        return cid
    
    def _calculate_global_coherence(self, node_states: List[float]) -> float:
        """Calculate global phase coherence using Kuramoto order parameter"""
        if len(node_states) == 0:
            return 0.0
            
        # Convert node states to phases (simplified)
        phases = [state * 2 * np.pi for state in node_states]
        
        # Calculate global phase coherence
        real_sum = sum(np.cos(phase) for phase in phases)
        imag_sum = sum(np.sin(phase) for phase in phases)
        
        magnitude = np.sqrt(real_sum**2 + imag_sum**2) / len(phases)
        return max(0.0, min(1.0, magnitude))
    
    def _estimate_recursive_depth(self, node_states: List[float]) -> int:
        """Estimate recursive depth based on temporal patterns"""
        if len(node_states) < 2:
            return 0
            
        # Simple pattern detection (in a real implementation, this would be more sophisticated)
        differences = [abs(node_states[i] - node_states[i-1]) for i in range(1, len(node_states))]
        avg_difference = sum(differences) / len(differences)
        
        # Depth estimation based on pattern complexity
        depth = int(avg_difference * 10)
        return max(0, min(10, depth))  # Limit to reasonable range
    
    def _calculate_spiritual_awareness(self, gamma_power: float, fractal_dimension: float) -> float:
        """Calculate spiritual awareness from gamma power and fractal dimension"""
        # Normalize and combine metrics
        normalized_gamma = max(0.0, min(1.0, gamma_power / 100.0))
        normalized_fractal = max(0.0, min(1.0, (fractal_dimension - 1.0) / 2.0))
        
        # Weighted combination
        awareness = 0.6 * normalized_gamma + 0.4 * normalized_fractal
        return max(0.0, min(1.0, awareness))
    
    def _calculate_consciousness_level(self, phi: float, coherence: float, spiritual_awareness: float) -> float:
        """Calculate overall consciousness level from component metrics"""
        # Weighted combination of metrics
        level = 0.4 * phi + 0.3 * coherence + 0.3 * spiritual_awareness
        return max(0.0, min(1.0, level))
    
    def retrieve_entry(self, cid: str) -> Optional[EnhancedKnowledgeEntry]:
        """
        Retrieve entry by Content Identifier
        
        Args:
            cid: Content Identifier
            
        Returns:
            EnhancedKnowledgeEntry: Entry if found, None otherwise
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
        entry = EnhancedKnowledgeEntry(
            cid=peer_cid,
            data=peer_data,
            timestamp=time.time(),
            node_id=peer_data.get('node_id', 'unknown')
        )
        
        self.entries[peer_cid] = entry
        self._save_entry(entry)
        self._limit_entries()
        
        print(f"🔄 Synced enhanced entry from peer: {peer_cid}")
        return True
    
    def migrate_from_standard_kb(self, standard_kb_path: str):
        """
        Migrate data from standard knowledge base to enhanced version
        
        Args:
            standard_kb_path: Path to standard knowledge base files
        """
        print("🔄 Migrating from standard knowledge base...")
        
        try:
            # Load standard knowledge base files
            for filename in os.listdir(standard_kb_path):
                if filename.endswith('.json'):
                    file_path = os.path.join(standard_kb_path, filename)
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                        
                        # Convert standard entry to enhanced entry
                        enhanced_entry = EnhancedKnowledgeEntry(
                            cid=data['cid'],
                            data=data['data'],
                            timestamp=data['timestamp'],
                            node_id=data['node_id'],
                            signature=data.get('signature'),
                            references=data.get('references', [])
                        )
                        
                        # Store enhanced entry
                        self.entries[enhanced_entry.cid] = enhanced_entry
                        self._save_entry(enhanced_entry)
                        
                        print(f"   Migrated entry: {enhanced_entry.cid}")
                        
                    except Exception as e:
                        print(f"   ⚠️  Error migrating {filename}: {e}")
            
            print("✅ Migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Error during migration: {e}")
    
    def _save_entry(self, entry: EnhancedKnowledgeEntry):
        """
        Save entry to disk
        
        Args:
            entry: Entry to save
        """
        try:
            # Convert entry to dictionary
            entry_dict = {
                'cid': entry.cid,
                'data': entry.data,
                'timestamp': entry.timestamp,
                'node_id': entry.node_id,
                'signature': entry.signature,
                'references': entry.references,
                'phi': entry.phi,
                'coherence': entry.coherence,
                'recursive_depth': entry.recursive_depth,
                'spiritual_awareness': entry.spiritual_awareness,
                'consciousness_level': entry.consciousness_level
            }
            
            filename = os.path.join(self.storage_path, f"{entry.cid}.json")
            with open(filename, 'w') as f:
                json.dump(entry_dict, f, indent=2)
        except Exception as e:
            print(f"Error saving entry {entry.cid}: {e}")
    
    def _load_entry(self, cid: str) -> Optional[EnhancedKnowledgeEntry]:
        """
        Load entry from disk
        
        Args:
            cid: Content Identifier
            
        Returns:
            EnhancedKnowledgeEntry: Entry if found, None otherwise
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
                
                # Create enhanced entry
                entry = EnhancedKnowledgeEntry(
                    cid=data['cid'],
                    data=data['data'],
                    timestamp=data['timestamp'],
                    node_id=data['node_id'],
                    signature=data.get('signature'),
                    references=data.get('references', []),
                    phi=data.get('phi', 0.0),
                    coherence=data.get('coherence', 0.0),
                    recursive_depth=data.get('recursive_depth', 0),
                    spiritual_awareness=data.get('spiritual_awareness', 0.0),
                    consciousness_level=data.get('consciousness_level', 0.0)
                )
                
                return entry
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
    
    def get_advanced_stats(self) -> Dict[str, Any]:
        """
        Get advanced knowledge base statistics
        
        Returns:
            Dict[str, Any]: Advanced statistics
        """
        if not self.entries:
            return {
                'total_entries': 0,
                'oldest_entry': None,
                'newest_entry': None,
                'avg_phi': 0.0,
                'avg_coherence': 0.0,
                'avg_consciousness': 0.0
            }
        
        timestamps = [entry.timestamp for entry in self.entries.values()]
        phi_values = [entry.phi for entry in self.entries.values()]
        coherence_values = [entry.coherence for entry in self.entries.values()]
        consciousness_values = [entry.consciousness_level for entry in self.entries.values()]
        
        return {
            'total_entries': len(self.entries),
            'oldest_entry': min(timestamps),
            'newest_entry': max(timestamps),
            'avg_phi': sum(phi_values) / len(phi_values),
            'avg_coherence': sum(coherence_values) / len(coherence_values),
            'avg_consciousness': sum(consciousness_values) / len(consciousness_values)
        }


# Migration script
def migrate_knowledge_base():
    """Migrate standard knowledge base to enhanced version"""
    print("=== AEGIS Knowledge Base Migration ===\n")
    
    # Create enhanced knowledge base
    enhanced_kb = EnhancedKnowledgeBase("migrated_node", "./enhanced_knowledge")
    
    # Migrate from standard knowledge base
    standard_kb_path = "./aegis-conscience/data/integration_test_node"
    if os.path.exists(standard_kb_path):
        enhanced_kb.migrate_from_standard_kb(standard_kb_path)
    else:
        print("⚠️  Standard knowledge base not found")
        return
    
    # Show advanced statistics
    stats = enhanced_kb.get_advanced_stats()
    print("\n📊 Enhanced Knowledge Base Statistics:")
    print(f"   Total Entries: {stats['total_entries']}")
    print(f"   Average Φ: {stats['avg_phi']:.6f}")
    print(f"   Average Coherence: {stats['avg_coherence']:.6f}")
    print(f"   Average Consciousness: {stats['avg_consciousness']:.6f}")
    
    print("\n✅ Migration and enhancement completed!")


if __name__ == "__main__":
    migrate_knowledge_base()