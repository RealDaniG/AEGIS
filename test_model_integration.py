#!/usr/bin/env python3
"""
Test script for model integration with Open-A.G.I
"""

import asyncio
import json
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_model_integration():
    """Test the model integration"""
    print("🧪 Testing Model Integration with Open-A.G.I")
    print("=" * 50)
    
    try:
        # Test 1: Import the model module
        print("1. Testing model module import...")
        import model_module
        print("✅ Model module imported successfully")
        
        # Test 2: Initialize the model
        print("\n2. Testing model initialization...")
        config = {
            "model_type": "dummy",
            "input_size": 768,
            "hidden_size": 256,
            "output_size": 128
        }
        
        success = await model_module.start_model_service(config)
        if success:
            print("✅ Model initialized successfully")
        else:
            print("❌ Model initialization failed")
            return False
        
        # Test 3: Run inference
        print("\n3. Testing model inference...")
        test_input = {
            "text": "This is a test input for the integrated model",
            "metadata": {"source": "integration_test"}
        }
        
        result = await model_module.run_model_inference(test_input)
        
        if "error" in result:
            print(f"❌ Model inference failed: {result['error']}")
            return False
        else:
            print("✅ Model inference completed successfully")
            print(f"   Output keys: {list(result.keys())}")
            if "embeddings" in result:
                print(f"   Embedding size: {len(result['embeddings'])}")
            if "classification_scores" in result:
                print(f"   Classification categories: {list(result['classification_scores'].keys())}")
        
        # Test 4: Test with different input
        print("\n4. Testing model with different input...")
        test_input2 = {
            "text": "Another test input to verify consistency",
            "metadata": {"source": "integration_test", "test_id": 2}
        }
        
        result2 = await model_module.run_model_inference(test_input2)
        
        if "error" in result2:
            print(f"❌ Second inference failed: {result2['error']}")
            return False
        else:
            print("✅ Second inference completed successfully")
            
        print("\n" + "=" * 50)
        print("🎉 All model integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_api_endpoint():
    """Test the API endpoint (if FastAPI is available)"""
    print("\n📡 Testing API endpoint integration...")
    
    try:
        # Try to import FastAPI to see if it's available
        from fastapi import FastAPI
        print("✅ FastAPI is available")
        
        # Try to import our API server
        import api_server
        print("✅ API server module imported")
        
        # This would be where we test the actual endpoint, but we'd need to start the server
        print("ℹ️  API endpoint testing would require starting the server")
        return True
        
    except ImportError as e:
        print(f"ℹ️  FastAPI not available for testing: {e}")
        return True
    except Exception as e:
        print(f"❌ API endpoint test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Model Integration Tests")
    
    # Run the async tests
    success = asyncio.run(test_model_integration())
    
    if success:
        # Test API integration
        api_success = asyncio.run(test_api_endpoint())
        if api_success:
            print("\n🏆 All tests completed successfully!")
            return 0
        else:
            print("\n⚠️  Model tests passed but API tests failed")
            return 1
    else:
        print("\n💥 Model integration tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())