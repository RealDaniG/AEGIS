# System Testing Guide

## Overview

This document provides instructions for running comprehensive tests on the Metatron AEGIS system to verify all components are working correctly.

## Prerequisites

Before running the tests, ensure that:

1. The Metatron system is running (typically via `run_metatron_web.ps1`)
2. All required Python packages are installed
3. The system is accessible at `http://localhost:8003`

## Running the Full System Test

### Method 1: Using the Batch Script (Windows)

```cmd
run_full_test.bat
```

### Method 2: Direct Python Execution

```bash
python full_system_test.py
```

## Test Categories

The comprehensive test suite validates the following components:

### 1. HTTP API Endpoints
- Health check endpoint (`/api/health`)
- Status endpoint (`/api/status`)
- Nodes endpoint (`/api/nodes`)
- Frequency info endpoint (`/api/frequency/info`)

### 2. WebSocket Connection
- Connection establishment
- Real-time data reception
- Consciousness metrics validation
- Node data structure verification

### 3. Static File Access
- Main UI page
- Integrated dashboard
- Streaming interface
- JavaScript bundles

### 4. Consciousness Engine
- Metrics calculation (Φ, R, C, γ)
- State classification
- Value range validation

### 5. Memory Integration
- MemoryMatrixNode (Node 3) detection
- Node list verification

### 6. P2P Networking
- Module import validation
- API endpoint availability

### 7. UI Integration
- Page loading
- Required element presence

## Interpreting Results

### Pass Criteria
- 80% or more test categories must pass
- All critical functionality must be operational

### Fail Criteria
- Less than 80% test categories pass
- Critical components (HTTP API, WebSocket) fail

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Ensure the Metatron system is running
   - Check that port 8003 is accessible
   - Verify firewall settings

2. **Module Import Errors**
   - Ensure all Python dependencies are installed
   - Check Python path configuration

3. **Timeout Errors**
   - System may be overloaded
   - Increase timeout values in the test script

### Debugging Steps

1. Run individual test categories to isolate issues
2. Check system logs for error messages
3. Verify all required services are running
4. Test network connectivity to localhost:8003

## Customization

The test script can be customized by modifying:

- Timeout values for API calls
- Success criteria thresholds
- Additional test endpoints
- Validation rules for metrics

## Automated Testing

For CI/CD integration, the script can be run in headless mode:

```bash
python full_system_test.py
```

The script will exit with:
- Code 0: All tests passed
- Code 1: Tests failed

## Reporting

Test results are displayed in the console with:
- Clear pass/fail indicators
- Detailed error messages
- Timing information
- Summary statistics