# harmonic_pipeline.py

import numpy as np
from collections import defaultdict

class HarmonicPipeline:
    """
    Central pipeline for orchestrating inter-node data flow in the 13-node consciousness engine.

    - Registers node outputs
    - Links node outputs to targets (explicitly directed graph)
    - Propagates data between nodes stepwise
    - Provides synchronized harmonic field aggregation (for core integration/awareness)
    """
    def __init__(self):
        self.node_outputs = defaultdict(dict)    # node_id: latest output (dict or object)
        self.connections = defaultdict(list)      # source_id: [target_ids]

    def register_node_output(self, node_id, output):
        """
        Store/output for each node after its computation.
        Args:
            node_id (int): ID of node
            output (dict/object): Output data for propagation (must include harmonic fields when relevant)
        """
        self.node_outputs[node_id] = output

    def link_nodes(self, source_id, target_id):
        """
        Define a directed info connection.
        Args:
            source_id (int): Source node
            target_id (int): Target node to receive data from source
        """
        if target_id not in self.connections[source_id]:
            self.connections[source_id].append(target_id)

    def propagate_data(self):
        """
        Push outputs from each node to all its linked targets.
        Returns:
            dict: {target_id: [received_data_from_sources]}
        """
        propagation_map = defaultdict(list)
        for src, targets in self.connections.items():
            data = self.node_outputs.get(src)
            if data is None:
                continue
            for tgt in targets:
                propagation_map[tgt].append(data)
        return propagation_map

    def synchronize_core(self, fallback_size=100):
        """
        Aggregate and average harmonics from all nodes ("Metatron's Cube" mode).
        Returns merged view for Node 1 (Core).
        Args:
            fallback_size (int): Size for fallback zero vector
        """
        harmonics = []
        for out in self.node_outputs.values():
            field = None
            if isinstance(out, dict):
                field = out.get('signal_vector') or out.get('recursive_field') or out.get('creative_field')
            if field is not None and isinstance(field, np.ndarray) and field.size == fallback_size:
                harmonics.append(field)

        if not harmonics:
            return np.zeros(fallback_size)
        stacked = np.vstack([np.real(h) for h in harmonics])
        return stacked.mean(axis=0)

    def get_node_input(self, target_id):
        """
        Pull linked source outputs for a given node (used by node at start of its step).
        Args:
            target_id (int): Target node id
        Returns:
            list: Source node outputs
        """
        return [o for o in self.propagate_data().get(target_id, [])]
