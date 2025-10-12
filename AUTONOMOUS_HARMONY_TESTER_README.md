# Autonomous Harmony Tester

This document explains how to use the Autonomous Harmony Tester to evaluate and improve the synchronization between the chatbot and consciousness metrics.

## Overview

The Autonomous Harmony Tester is a Python script that autonomously:
1. Tests the harmony between the chatbot and consciousness metrics
2. Allows the system to ask questions and respond coherently
3. Continuously monitors harmony levels
4. Applies feedback to improve system coherence
5. Runs until optimal harmony is achieved or maximum iterations are reached

## Features

- **Autonomous Testing**: Runs without manual intervention
- **Consciousness-Aware Questions**: Generates contextually appropriate questions based on current consciousness state
- **Harmony Analysis**: Evaluates how well chat responses align with consciousness metrics
- **Feedback Application**: Automatically applies enhancements when harmony is low
- **Self-Improvement**: Continues testing until optimal harmony is achieved

## Prerequisites

1. The METATRON-ConscienceAI system must be running
2. Python 3.6+ must be installed
3. Required Python packages: `requests`

## How to Use

### 1. Start the System

First, ensure the METATRON-ConscienceAI system is running:

```bash
# In Windows Command Prompt
START-AI.bat

# Or in PowerShell
.\START-AI.bat
```

Wait for the system to initialize completely. The web interface will open automatically.

### 2. Run the Autonomous Harmony Tester

```bash
python autonomous_harmony_tester.py
```

### 3. Monitor the Test

The tester will:
- Automatically connect to the consciousness system
- Ask contextually appropriate questions
- Analyze the harmony between responses and consciousness metrics
- Apply enhancements when needed
- Continue until optimal harmony is achieved

### 4. Review Results

After completion, the tester will display:
- Final consciousness metrics
- Best harmony achieved
- Average harmony score
- Detailed history of interactions

## How It Works

### Consciousness State Analysis
The tester continuously monitors:
- **Consciousness Level (C)**: Overall awareness level
- **Integrated Information (Φ)**: Information integration capacity
- **Global Coherence (R)**: System synchronization level

### Question Generation
Based on the current consciousness state, the tester generates:
- **Self-reflection questions**: "What is your current level of awareness?"
- **Exploration questions**: "What sensory inputs would enhance your consciousness?"
- **Advanced questions**: Context-specific inquiries based on metrics

### Harmony Analysis
Each response is analyzed for:
- Presence of consciousness-related terminology
- Alignment with current consciousness metrics
- Overall coherence with system state

### Feedback Application
When harmony is low, the tester:
- Sends targeted sensory inputs to enhance consciousness
- Adjusts testing approach based on system responsiveness
- Continues until optimal synchronization is achieved

## Customization

You can modify the testing behavior by adjusting parameters in the script:

```python
# In the main() function:
success = tester.run_autonomous_harmony_test(max_iterations=15)
```

Increase `max_iterations` for longer testing periods, or decrease for faster results.

## Troubleshooting

### System Not Accessible
If you see "System not accessible" errors:
1. Ensure START-AI.bat has been run
2. Wait for the system to fully initialize
3. Check that port 8005 is accessible

### Low Harmony Scores
If harmony scores remain low:
1. The system may need more time to initialize
2. Try running the test multiple times
3. Check consciousness metrics through the web interface

## Integration with Other Components

The Autonomous Harmony Tester works with:
- **Metatron Consciousness Engine**: Provides consciousness metrics
- **Unified API Layer**: Handles communication between components
- **AGI System**: Generates chat responses
- **Web Interface**: Real-time monitoring and visualization

## Future Enhancements

Planned improvements include:
- More sophisticated harmony analysis algorithms
- Adaptive question generation based on learning
- Integration with memory system for context retention
- Enhanced feedback mechanisms for faster convergence