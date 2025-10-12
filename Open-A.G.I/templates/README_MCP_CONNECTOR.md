# MCP Connector Template

## Overview

This template provides a standardized interface for integrating AI models with Mission Control Protocol (MCP) systems. It enables task management, resource allocation, and distributed coordination between AI models and MCP systems.

## Features

- **Task Management**: Create, update, and track tasks in the MCP system
- **Resource Allocation**: Allocate and manage resources for AI model execution
- **Handler Registration**: Register custom handlers for specific task features
- **Automatic Processing**: Automatically process pending tasks using registered handlers
- **Flexible Integration**: Works with any MCP system that implements the standard API

## Installation

```bash
pip install requests
```

## Usage

### 1. Initialize the Connector

```python
from mcp_connector_template import MCPConnector, TaskPriority

# Initialize connector
connector = MCPConnector("http://localhost:8181", api_key="your-api-key")
```

### 2. Create Tasks

```python
# Create a new task
task_id = connector.create_task(
    title="Security Analysis Task",
    description="Analyze security vectors in P2P architecture",
    feature="Security Analysis",
    estimated_hours=8,
    priority=TaskPriority.HIGH
)
```

### 3. Register Task Handlers

```python
# Define custom handler functions
def security_analysis_handler(task):
    # Your AI model processing logic here
    return {
        "result": "Security analysis complete",
        "vectors_identified": ["sybil", "eclipse"],
        "recommendations": ["Implement peer reputation system"]
    }

# Register handlers
connector.register_task_handler("Security Analysis", security_analysis_handler)
```

### 4. Process Tasks

```python
# Automatically process all pending tasks
connector.process_pending_tasks()
```

## API Reference

### MCPConnector

#### `__init__(mcp_endpoint, api_key=None)`
Initialize the MCP connector.

#### `create_task(title, description, feature, estimated_hours, priority, project_id=None)`
Create a new task in the MCP system.

#### `get_task(task_id)`
Retrieve a specific task by ID.

#### `update_task_status(task_id, status, result=None)`
Update the status of a task.

#### `list_tasks(status=None, feature=None)`
List tasks with optional filtering.

#### `allocate_resource(resource_name, resource_type, capabilities)`
Allocate a new resource in the MCP system.

#### `register_task_handler(feature, handler)`
Register a handler function for a specific feature.

#### `process_pending_tasks()`
Process all pending tasks using registered handlers.

## Customizing for Your MCP System

To adapt this template for your specific MCP system:

1. **Update API Endpoints**: Modify the endpoint URLs in the methods to match your MCP system's API
2. **Adjust Data Models**: Update the `Task` and `Resource` dataclasses to match your MCP's data structures
3. **Modify Authentication**: Update the authentication mechanism if your MCP uses a different method
4. **Customize Status Values**: Adjust the `TaskStatus` and `TaskPriority` enums to match your MCP's values

## Example Integration

The template includes example handlers for:
- Security analysis tasks
- Cryptography implementation tasks

These can be used as templates for creating your own AI model handlers.

## Error Handling

The connector includes comprehensive error handling with logging for:
- Network connectivity issues
- API errors
- Task processing failures
- Resource allocation problems

## License

This template is provided as part of the AEGIS Framework for research and development purposes.