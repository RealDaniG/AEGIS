from cryptography.hazmat.primitives.asymmetric import ed25519
from improved_pbft_consensus import MetatronAwarePBFT

# Create test node
private_key = ed25519.Ed25519PrivateKey.generate()
consensus = MetatronAwarePBFT('test_node_0', private_key)
print('Initial nodes:', len(consensus.known_nodes))

# Add the test node itself to known nodes
consensus.add_node('test_node_0', private_key.public_key())
print('After adding self:', len(consensus.known_nodes))

# Add test nodes (12 additional nodes for 13 total)
for i in range(1, 13):
    other_key = ed25519.Ed25519PrivateKey.generate()
    other_id = f'test_node_{i}'
    consensus.add_node(other_id, other_key.public_key())
    
print('Final nodes:', len(consensus.known_nodes))
print('Node IDs:', list(consensus.known_nodes.keys()))