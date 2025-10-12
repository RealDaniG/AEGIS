# Project Structure Documentation

This document explains the organized structure of the Metatron V2 + Open A.G.I. project after cleanup and reorganization.

## Directory Structure

```
METATRONV2/
├── Metatron-ConscienceAI/          # Core consciousness engine with 13-node sacred geometry
├── Open-A.G.I/                     # Open Artificial General Intelligence framework
├── aegis-conscience/               # AEGIS security framework with consciousness features
├── consensus_tools/                # Consensus algorithm implementations and tools
├── docs/                           # All documentation files
├── enhanced_knowledge/             # Enhanced knowledge base components
├── integration_tools/              # Integration testing and demonstration tools
├── knowledge_base_tools/           # Knowledge base enhancement tools
├── tests/                          # All test files organized by functionality
├── visualization_tools/            # Visualization tools and monitoring systems
├── data/                           # Data storage directory
├── requirements.txt                # Project dependencies
└── README.md                      # Main project overview
```

## Directory Descriptions

### consensus_tools/
Contains all consensus algorithm implementations and related tools:
- `improved_pbft_consensus.py` - Enhanced PBFT implementation for 13-node system

### docs/
Contains all documentation files:
- Integration documentation
- System architecture guides
- API documentation
- Deployment guides
- Research papers and theory documentation

### integration_tools/
Contains tools for integration testing and demonstrations:
- `demonstrate_integration.py` - Integration demonstration scripts
- `demonstration.py` - General demonstration tools
- `onion_address_demo.py` - Onion address demonstration
- `verify_real_data.py` - Data authenticity verification tools

### knowledge_base_tools/
Contains tools for knowledge base enhancement:
- `enhanced_knowledge_base.py` - Enhanced knowledge base implementation
- `knowledge_base_enhancer.py` - Knowledge base enhancement tools

### tests/
Contains all test files organized by functionality:
- Unit tests for various components
- Integration tests
- Specialized testing tools

### visualization_tools/
Contains all visualization tools and monitoring systems:
- `comprehensive_node_monitor.py` - Detailed node monitoring
- `data_validation_tool.py` - Data authenticity verification
- `improved_visualizer.py` - Enhanced visualization rendering
- `metatron_node_visualizer.py` - Node visualization tools
- `metatron_simple_visualizer.py` - Simple visualization
- `robust_realtime_visualizer.py` - Primary visualization tool
- `sacred_geometry_monitor.py` - Sacred geometry monitoring

### Root Level Files
- `requirements.txt` - Project dependencies
- `README.md` - Main project overview

## Module Directories

### Metatron-ConscienceAI/
The core consciousness engine implementing the 13-node network based on Metatron's Cube geometry.

### Open-A.G.I/
The Open Artificial General Intelligence framework with distributed consensus protocols and AI capabilities.

### aegis-conscience/
The AEGIS security framework with consciousness features and TOR integration.

### enhanced_knowledge/
Enhanced knowledge base components for the system.

### data/
Data storage directory for metrics and other data files.

## Benefits of This Structure

1. **Clear Organization**: Files are grouped by functionality making it easier to navigate
2. **Separation of Concerns**: Different aspects of the system are isolated in their own directories
3. **Scalability**: New tools and components can be easily added to the appropriate directories
4. **Maintainability**: Easier to maintain and update specific components without affecting others
5. **Testing**: All tests are centralized in one location while maintaining logical grouping

This structure makes it easier for developers to find what they're looking for and understand the relationships between different components of the system.