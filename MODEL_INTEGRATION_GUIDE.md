# Model Integration Guide for Open-A.G.I

## Overview

This guide explains how to integrate custom AI models with the Open-A.G.I decentralized application framework. The integration allows models to leverage the distributed computing, privacy-preserving features, and consensus mechanisms of the Open-A.G.I network.

## Architecture

The Open-A.G.I system uses a modular architecture where each component is loaded dynamically:

1. **Modules** are imported and initialized through the `main.py` entry point
2. Each module exposes specific async functions for initialization
3. **Configuration** is managed through `app_config.json`
4. The system supports **distributed learning** through the `distributed_learning.py` module
5. **API endpoints** are provided through `api_server.py`

## Integration Steps

### 1. Create Your Model Module

Create a new Python module that encapsulates your model following the existing patterns:

```python
# model_module.py
import asyncio
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CustomModel:
    def __init__(self):
        self.model = None
        self.config = {}
        self.is_initialized = False
        
    async def initialize(self, config: Dict[str, Any]):
        """Initialize the model with configuration"""
        self.config = config
        # Load your model here
        # self.model = load_your_model(config["model_path"])
        self.is_initialized = True
        return True
    
    async def inference(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run inference on input data"""
        if not self.is_initialized:
            return {"error": "Model not initialized"}
        
        # Process input through your model
        # result = self.model.process(input_data)
        # return result
        pass

# Global model instance
model_instance = CustomModel()

# Module functions for Open-A.G.I integration
async def start_model_service(config: Dict[str, Any]):
    """Start the model service"""
    return await model_instance.initialize(config)

async def run_model_inference(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Run inference using the model"""
    return await model_instance.inference(input_data)
```

### 2. Register Your Model Module

Add your model module to the main initialization sequence in `main.py`:

```python
# In main.py start_node function, add after other module imports:
model_mod, model_err = safe_import("model_module")

# Add error handling:
if model_err:
    logger.warning(f"Modelo personalizado no disponible: {model_err}")

# Add initialization in the startup sequence:
# Inicializar Modelo Personalizado
if cfg["app"]["enable"].get("model") and model_mod:
    try:
        logger.info("🚀 Iniciando modelo personalizado...")
        await module_call(model_mod, "start_model_service", cfg.get("model", {}))
        logger.info("✅ Modelo personalizado iniciado")
    except Exception as e:
        logger.error(f"❌ Error iniciando modelo personalizado: {e}")
```

### 3. Update Configuration

Add model configuration to `app_config.json`:

```json
{
  "app": {
    "enable": {
      "model": true
    }
  },
  "model": {
    "model_path": "./models/your_model.pth",
    "model_type": "your_model_type",
    "max_tokens": 2048,
    "temperature": 0.7
  }
}
```

### 4. Add API Endpoints

Add API endpoints for your model in `api_server.py`:

```python
# In the _add_default_routes method:
# Add model inference endpoint
@self.app.post("/model/inference")
async def model_inference(request: Request):
    try:
        # Import the model module function
        import sys
        import importlib
        model_module = importlib.import_module("model_module")
        
        data = await request.json()
        result = await model_module.run_model_inference(data)
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Model API Error: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
```

### 5. Add to Module List

Add your model module to the list of modules in the CLI command:

```python
# In the list_modules command:
mods = [
    # ... other modules
    "model_module",
]
```

## Example Implementation

Here's a complete example of a model module integration:

### model_module.py
```python
#!/usr/bin/env python3
"""
Custom Model Integration for Open-A.G.I
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional
import torch
import numpy as np

logger = logging.getLogger(__name__)

class CustomModel:
    def __init__(self):
        self.model = None
        self.config = {}
        self.is_initialized = False
        
    async def initialize(self, config: Dict[str, Any]):
        """Initialize the model with configuration"""
        self.config = config
        model_type = config.get("model_type", "dummy")
        
        try:
            logger.info(f"Initializing {model_type} model")
            
            if model_type == "dummy":
                # Create a simple dummy model for demonstration
                self.model = DummyModel()
            elif model_type == "neural_network":
                # Create a simple neural network
                self.model = SimpleNeuralNetwork(
                    input_size=config.get("input_size", 768),
                    hidden_size=config.get("hidden_size", 256),
                    output_size=config.get("output_size", 128)
                )
            else:
                # Fallback to dummy model
                logger.warning(f"Unknown model type {model_type}, using dummy model")
                self.model = DummyModel()
            
            self.is_initialized = True
            logger.info("✅ Model initialized successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Error initializing model: {e}")
            return False
    
    async def inference(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run inference on input data"""
        if not self.is_initialized or not self.model:
            return {"error": "Model not initialized"}
        
        try:
            # Process input based on model type
            result = self.model.forward(input_data)
            
            # Add metadata
            result["model_type"] = self.config.get("model_type", "unknown")
            result["timestamp"] = asyncio.get_event_loop().time()
            
            return result
        except Exception as e:
            logger.error(f"❌ Error during inference: {e}")
            return {"error": str(e)}

class DummyModel:
    """A simple dummy model for demonstration purposes"""
    
    def forward(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return dummy output"""
        # Extract text if present
        text = input_data.get("text", "")
        
        # Generate dummy embeddings (simulating model output)
        embedding_size = 128
        embeddings = np.random.rand(embedding_size).tolist()
        
        # Generate dummy classification scores
        categories = ["positive", "negative", "neutral"]
        scores = {cat: float(np.random.rand()) for cat in categories}
        
        return {
            "input_text": text,
            "embeddings": embeddings,
            "classification_scores": scores,
            "confidence": float(np.random.rand())
        }

class SimpleNeuralNetwork(torch.nn.Module):
    """A simple neural network for demonstration"""
    
    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        super(SimpleNeuralNetwork, self).__init__()
        self.fc1 = torch.nn.Linear(input_size, hidden_size)
        self.fc2 = torch.nn.Linear(hidden_size, hidden_size)
        self.fc3 = torch.nn.Linear(hidden_size, output_size)
        self.relu = torch.nn.ReLU()
        self.dropout = torch.nn.Dropout(0.1)
        
    def forward(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input through the neural network"""
        # For demonstration, we'll create a random input tensor
        batch_size = 1
        input_tensor = torch.randn(batch_size, self.fc1.in_features)
        
        # Forward pass
        x = self.relu(self.fc1(input_tensor))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        output = self.fc3(x)
        
        # Convert to list for JSON serialization
        output_list = output.detach().cpu().numpy().flatten().tolist()
        
        return {
            "input_shape": input_tensor.shape,
            "output": output_list,
            "output_size": len(output_list)
        }

# Global model instance
model_instance = CustomModel()

# Module functions for Open-A.G.I integration
async def start_model_service(config: Dict[str, Any]):
    """Start the model service"""
    logger.info("🚀 Starting custom model service...")
    success = await model_instance.initialize(config)
    if success:
        logger.info("✅ Custom model service started")
    else:
        logger.error("❌ Failed to start custom model service")
    return success

async def run_model_inference(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Run inference using the model"""
    logger.info(f"🧠 Running model inference on input: {input_data.get('text', 'N/A')}")
    result = await model_instance.inference(input_data)
    logger.info("✅ Model inference completed")
    return result
```

## Distributed Learning Integration

To leverage the distributed learning capabilities:

1. Extend the `ModelUpdate` dataclass in `distributed_learning.py` to support your model's parameters
2. Implement gradient computation for your model
3. Add your model to the aggregation methods

Example extension for distributed learning:
```python
# In distributed_learning.py, extend ModelUpdate:
@dataclass
class ModelUpdate:
    # ... existing fields ...
    custom_model_params: Optional[Dict[str, Any]] = None
```

## Consciousness Integration

If your model has consciousness-related features, integrate with the consciousness engine:

1. Add consciousness metrics to the `ConsciousnessState` dataclass
2. Create periodic consciousness state updates
3. Store consciousness data in the memory system

## Testing

Create unit tests for your model module:

```python
# tests/test_model_module.py
import pytest
import asyncio
from model_module import CustomModel

@pytest.mark.asyncio
async def test_model_initialization():
    model = CustomModel()
    config = {"model_path": "bert-base-uncased"}
    result = await model.initialize(config)
    assert result == True

@pytest.mark.asyncio
async def test_model_inference():
    model = CustomModel()
    config = {"model_path": "bert-base-uncased"}
    await model.initialize(config)
    
    result = await model.inference({"text": "Hello, world!"})
    assert "embeddings" in result
    assert isinstance(result["embeddings"], list)
```

## Deployment

### Requirements
Add your model dependencies to `requirements.txt`:
```
torch>=1.9.0
transformers>=4.12.0
# Add any other dependencies your model needs
```

### Docker Integration
Update the Dockerfile to include model files:
```dockerfile
# Copy model files
COPY models/ ./models/
```

## Monitoring

### Metrics Integration
Add model performance metrics to `metrics_collector.py`:
```python
class ModelMetrics:
    def __init__(self):
        self.inference_count = 0
        self.average_latency = 0.0
        self.error_count = 0
```

### Dashboard Integration
Add model monitoring to the web dashboard:
- Inference throughput
- Error rates
- Latency metrics
- Model version information

## Security Considerations

1. **Input Validation**: Validate all inputs to prevent injection attacks
2. **Rate Limiting**: Implement rate limiting for model inference endpoints
3. **Authentication**: Add authentication for sensitive operations
4. **Privacy**: Ensure model outputs don't leak sensitive information

## Performance Optimization

1. **Caching**: Implement caching for frequent inputs
2. **Batching**: Support batch inference for better throughput
3. **Model Quantization**: Consider quantization for faster inference
4. **GPU Optimization**: Optimize for GPU usage when available

## Troubleshooting

### Common Issues

1. **Module Import Errors**
   - Ensure your model module is in the Python path
   - Check that all dependencies are installed

2. **Configuration Issues**
   - Verify the model configuration in `app_config.json`
   - Ensure all required configuration parameters are present

3. **API Endpoint Issues**
   - Check that FastAPI is properly installed
   - Verify that the API server is running

### Debugging Tips

1. Enable debug logging to see detailed error messages
2. Test your model module independently before integration
3. Use the test scripts to verify each component

## Best Practices

1. **Modular Design**: Keep your model implementation separate from the integration code
2. **Error Handling**: Implement comprehensive error handling for all operations
3. **Logging**: Add detailed logging for debugging and monitoring
4. **Configuration**: Make your model configurable through the standard configuration system
5. **Testing**: Write comprehensive tests for your model integration
6. **Documentation**: Document your model's API and usage

## Next Steps

1. Implement your specific model in the `CustomModel` class
2. Add any required dependencies to `requirements.txt`
3. Configure your model parameters in `app_config.json`
4. Test the integration thoroughly
5. Add monitoring and metrics collection
6. Document your model's specific features and capabilities

This integration approach maintains compatibility with the existing Open-A.G.I architecture while providing a clean integration point for your custom model.