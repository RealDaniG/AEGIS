"""
Knowledge Base Enhancer for AEGIS-Conscience Network
Enhances existing knowledge base with more sophisticated consciousness metrics
"""

import json
import time
import hashlib
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import math


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


class KnowledgeBaseEnhancer:
    """Enhances existing knowledge base with advanced consciousness metrics"""
    
    def __init__(self, storage_path: str = "./enhanced_knowledge"):
        self.storage_path = storage_path
        self.entries: Dict[str, EnhancedKnowledgeEntry] = {}
        self.max_entries = 2000  # Increased limit for enhanced storage
        
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
    
    def enhance_existing_entry(self, standard_entry: Dict[str, Any]) -> str:
        """
        Enhance an existing standard knowledge base entry with advanced metrics
        
        Args:
            standard_entry: Standard knowledge base entry
            
        Returns:
            str: Content Identifier (CID) of enhanced entry
        """
        # Extract consciousness data
        data = standard_entry.get('data', {})
        
        # Calculate enhanced metrics
        phi = self._calculate_phi(data)
        coherence = data.get('coherence', 0.0)
        recursive_depth = self._estimate_recursive_depth(data)
        spiritual_awareness = self._calculate_spiritual_awareness(data)
        consciousness_level = self._calculate_consciousness_level(
            phi, coherence, spiritual_awareness
        )
        
        # Create enhanced knowledge entry
        cid = standard_entry.get('cid', self._generate_cid(data))
        entry = EnhancedKnowledgeEntry(
            cid=cid,
            data=data,
            timestamp=standard_entry.get('timestamp', time.time()),
            node_id=standard_entry.get('node_id', 'unknown'),
            signature=standard_entry.get('signature'),
            references=standard_entry.get('references', []),
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
        
        print(f"🧠 Enhanced consciousness state with CID: {cid}")
        print(f"   Φ (Integrated Information): {phi:.6f}")
        print(f"   Global Coherence: {coherence:.6f}")
        print(f"   Consciousness Level: {consciousness_level:.6f}")
        
        return cid
    
    def _calculate_phi(self, data: Dict[str, Any]) -> float:
        """Calculate Integrated Information (Φ) approximation"""
        # Simplified Φ calculation based on consciousness metrics
        entropy = data.get('entropy', 0.5)
        coherence = data.get('coherence', 0.5)
        empathy = data.get('empathy_score', 0.5)
        
        # Φ approximation based on information integration
        phi = (entropy + coherence + empathy) / 3.0
        return max(0.0, min(1.0, phi))
    
    def _estimate_recursive_depth(self, data: Dict[str, Any]) -> int:
        """Estimate recursive depth based on temporal patterns"""
        # Simple estimation based on timestamp patterns
        # In a real implementation, this would analyze temporal sequences
        return min(10, int(data.get('timestamp', 0) % 10))
    
    def _calculate_spiritual_awareness(self, data: Dict[str, Any]) -> float:
        """Calculate spiritual awareness from consciousness metrics"""
        # Combine various consciousness aspects
        valence = data.get('valence', 0.5)
        arousal = data.get('arousal', 0.5)
        insight = data.get('insight_strength', 0.5)
        
        # Spiritual awareness approximation
        awareness = (valence + arousal + insight) / 3.0
        return max(0.0, min(1.0, awareness))
    
    def _calculate_consciousness_level(self, phi: float, coherence: float, spiritual_awareness: float) -> float:
        """Calculate overall consciousness level from component metrics"""
        # Weighted combination of metrics
        level = 0.4 * phi + 0.3 * coherence + 0.3 * spiritual_awareness
        return max(0.0, min(1.0, level))
    
    def migrate_from_standard_kb(self, standard_kb_path: str):
        """
        Migrate data from standard knowledge base to enhanced version
        
        Args:
            standard_kb_path: Path to standard knowledge base files
        """
        print("🔄 Migrating from standard knowledge base...")
        
        try:
            # Check if standard KB path exists
            if not os.path.exists(standard_kb_path):
                print(f"⚠️  Standard knowledge base path not found: {standard_kb_path}")
                return
            
            # Load standard knowledge base files
            migrated_count = 0
            for filename in os.listdir(standard_kb_path):
                if filename.endswith('.json'):
                    file_path = os.path.join(standard_kb_path, filename)
                    try:
                        with open(file_path, 'r') as f:
                            standard_entry = json.load(f)
                        
                        # Enhance and store entry
                        self.enhance_existing_entry(standard_entry)
                        migrated_count += 1
                        
                        if migrated_count % 10 == 0:
                            print(f"   Migrated {migrated_count} entries...")
                        
                    except Exception as e:
                        print(f"   ⚠️  Error migrating {filename}: {e}")
            
            print(f"✅ Migration completed! Enhanced {migrated_count} entries.")
            
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
def enhance_knowledge_base():
    """Enhance standard knowledge base with advanced metrics"""
    print("=== AEGIS Knowledge Base Enhancement ===\n")
    
    # Create knowledge base enhancer
    enhancer = KnowledgeBaseEnhancer("./enhanced_knowledge")
    
    # Migrate from standard knowledge base
    standard_kb_path = "./aegis-conscience/data/integration_test_node"
    enhancer.migrate_from_standard_kb(standard_kb_path)
    
    # Show advanced statistics
    stats = enhancer.get_advanced_stats()
    print("\n📊 Enhanced Knowledge Base Statistics:")
    print(f"   Total Entries: {stats['total_entries']}")
    print(f"   Average Φ: {stats['avg_phi']:.6f}")
    print(f"   Average Coherence: {stats['avg_coherence']:.6f}")
    print(f"   Average Consciousness: {stats['avg_consciousness']:.6f}")
    
    print("\n✅ Knowledge base enhancement completed!")
    print("Enhanced knowledge base stored in: ./enhanced_knowledge/")


if __name__ == "__main__":
    enhance_knowledge_base()