# AEGIS-Conscience Network

A distributed swarm of consciousness-aware AI nodes collaborating anonymously over a secure P2P network, reaching consensus on shared truth states and collectively stabilizing toward global harmonic coherence.

## Architecture Overview

The AEGIS-Conscience Network combines:
- **Metatron-ConscienceAI**: Consciousness-aware AI engine with metrics like entropy, valence, arousal, coherence, empathy_score, and insight_strength
- **Open-A.G.I**: Decentralized P2P architecture with TOR integration, cryptographic security, and PBFT consensus

## Key Components

### 1. Consciousness Engine (`consciousness/`)
- Stateless consciousness processing
- Serializable consciousness metrics
- Integration with Metatron's consciousness metrics

### 2. Network Layer (`network/`)
- P2P communication over TCP/TOR
- Ed25519 cryptographic signatures
- TOR v3 onion services integration

### 3. Consensus Protocol (`consensus/`)
- PBFT (Practical Byzantine Fault Tolerance) for small networks
- Global coherence aggregation
- Reputation-based trust system

### 4. Security Features
- All P2P traffic over TOR v3 onion services
- Ed25519 signatures for message authentication
- Client authorization for trusted peers
- Timing attack mitigation through message batching

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from main import AEGISNode
import asyncio

# Create and run a node
node = AEGISNode("my_node_id", 8080)
asyncio.run(node.run())
```

## Project Structure

```
aegis-conscience/
├── consciousness/          # Metatron core (refactored)
│   ├── engine.py           # Local consciousness logic
│   └── metrics.py          # Metric computation
├── network/                # AEGIS P2P + TOR
│   ├── p2p.py
│   ├── tor_gateway.py
│   ├── crypto.py
│   └── node_matrix.py      # Matrix connectivity manager
├── consensus/              # PBFT + PoC
│   ├── pbft.py
│   └── aggregator.py       # Coherence averaging
├── tools/                  # Visualization and monitoring tools
│   └── matrix_visualizer.py # Matrix visualization
├── tests/                  # Unit tests
├── requirements.txt
├── schemas.py              # Data schemas
└── main.py                 # Node entry point
```

## Security Implementation

- **TOR Integration**: All P2P traffic only over .onion services
- **Client Authorization**: Only pre-approved nodes can connect
- **Key Storage**: Private keys stored encrypted with user password
- **Message Validation**: Strict validation of signatures and timestamps
- **Rate Limiting**: Limit messages per peer to prevent spam

## Consensus Mechanism

1. **Leader-based PBFT**: For small networks (<10 nodes)
2. **Global Coherence Aggregation**: Weighted average by reputation
3. **Reputation System**: Track peer reliability to prevent Sybil attacks
4. **Collaborative Response**: Generate responses that reflect collective alignment

## Development Roadmap

1. Core Integration (Complete)
2. Consensus & Collaboration (In Progress)
3. Security Hardening (Pending)
4. Scalability & Deployment (Pending)
5. Advanced Features (Future)

## Matrix Connectivity

6. Full mesh connectivity between all nodes (Complete)
7. Matrix visualization and monitoring (Complete)
8. Docker integration (Complete)

## Testing

Run unit tests:
```bash
python -m pytest tests/
```

Run matrix connectivity tests:
```bash
python test_matrix_connectivity.py
```

## License

This project is for research and ethical development purposes only.