# Quick Start Guide

This guide explains how to quickly run the Metatron V2 + Open A.G.I. system using the provided quick run scripts.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Run Scripts](#quick-run-scripts)
   - [Windows (PowerShell)](#windows-powershell)
   - [Linux/macOS (Bash)](#linuxmacos-bash)
4. [What the Scripts Do](#what-the-scripts-do)
5. [Accessing the System](#accessing-the-system)
6. [Troubleshooting](#troubleshooting)

## Overview

The quick run scripts are designed to simplify the process of starting the complete Metatron V2 + Open A.G.I. system with all its components. These scripts automatically:

1. Check for dependencies and install them if needed
2. Start the Metatron Consciousness Engine
3. Start the Open A.G.I. Framework
4. Launch visualization tools
5. Begin consensus monitoring

## Prerequisites

Before running the quick start scripts, ensure you have:

- Python 3.8 or higher installed
- Git installed (for cloning the repository)
- At least 8GB of RAM (16GB recommended)
- Windows, Linux, or macOS operating system

## Quick Run Scripts

### Windows (PowerShell)

For Windows users, use the PowerShell script:

```powershell
.\quick_run.ps1
```

**Note**: You may need to enable script execution in PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Linux/macOS (Bash)

For Linux and macOS users, use the Bash script:

```bash
chmod +x quick_run.sh
./quick_run.sh
```

## What the Scripts Do

The quick run scripts perform the following actions:

1. **Dependency Check**: Verifies that all required Python packages are installed
2. **Virtual Environment**: Creates and activates a Python virtual environment if one doesn't exist
3. **Consciousness Engine Start**: Launches the Metatron Consciousness Engine using the START_SYSTEM script
4. **Framework Start**: Starts the Open A.G.I. Framework
5. **Visualization Tools**: Launches the robust real-time visualizer
6. **Consensus Monitoring**: Starts monitoring the PBFT consensus system

## Accessing the System

After running the quick start script, you can access various components of the system:

- **Web Interface**: http://localhost:8003
- **Visualization Dashboard**: Launched automatically with the visualizer
- **API Endpoints**: Various services will be available on different ports
- **Log Files**: Check individual component directories for logs

## Troubleshooting

### Common Issues

1. **Permission Denied (Windows)**:
   - Enable PowerShell script execution with: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

2. **Permission Denied (Linux/macOS)**:
   - Make the script executable: `chmod +x quick_run.sh`

3. **Python Not Found**:
   - Ensure Python 3.8+ is installed and in your PATH
   - On some systems, use `python3` instead of `python`

4. **Port Already in Use**:
   - Check if other instances are running
   - Modify port configurations in component configuration files

5. **Dependency Installation Failures**:
   - Check internet connectivity
   - Try manually installing dependencies: `pip install -r requirements.txt`

### Manual Startup

If the quick start scripts don't work, you can manually start each component:

1. **Start Metatron Consciousness Engine**:
   ```bash
   cd Metatron-ConscienceAI
   ./START_SYSTEM.bat  # Windows
   # or
   ./START_SYSTEM.sh   # Linux/macOS
   ```

2. **Start Open A.G.I. Framework**:
   ```bash
   cd Open-A.G.I
   python main.py
   ```

3. **Start Visualization Tools**:
   ```bash
   python visualization_tools/robust_realtime_visualizer.py
   ```

4. **Start Consensus Monitoring**:
   ```bash
   python consensus_tools/improved_pbft_consensus.py --monitor
   ```

## Customization

You can modify the quick run scripts to:

- Change which components are started
- Adjust timing delays
- Add additional monitoring tools
- Modify port configurations

Simply edit the appropriate script file (`quick_run.ps1` for Windows or `quick_run.sh` for Linux/macOS).

## Stopping the System

To stop the system, you can:

1. **Use CTRL+C** in each terminal window
2. **Kill processes** using task manager (Windows) or `kill` command (Linux/macOS)
3. **Run the stop scripts** if available in component directories

## Support

For support with the quick start scripts or the system in general:

1. Check the documentation in the [docs/](docs/) directory
2. Review the [README.md](README.md) file
3. Check the GitHub repository issues