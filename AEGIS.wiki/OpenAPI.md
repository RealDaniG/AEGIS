# OpenAPI in AEGIS

OpenAPI is a specification for building APIs that allows both humans and computers to understand the capabilities of a service without requiring access to source code, additional documentation, or inspection of network traffic.

## What is OpenAPI?

OpenAPI (formerly known as Swagger) is a language-agnostic interface description for HTTP APIs that allows both humans and computers to understand the capabilities of a service without requiring access to source code, additional documentation, or inspection of network traffic.

## OpenAPI in AEGIS Context

In AEGIS, OpenAPI plays a crucial role in providing standardized interfaces for interacting with both the consciousness engine and the AGI framework. The system exposes RESTful endpoints that follow OpenAPI specifications, making it easier for developers to integrate with AEGIS components.

### Key Benefits

1. **Standardization**: Consistent API design across all AEGIS components
2. **Documentation**: Automatically generated, interactive API documentation
3. **Tooling**: Support for code generation, testing, and validation
4. **Interoperability**: Easy integration with external systems and tools

## AEGIS OpenAPI Endpoints

### Unified API Server (Port 8003)
The main API server provides access to both consciousness and AGI functionalities:

- `GET /api/consciousness` - Real-time consciousness metrics
- `GET /api/agi` - AGI system status and capabilities
- `POST /api/input` - Send sensory input to consciousness system
- `POST /api/chat` - Send chat message to AGI system
- `GET /api/health` - System health check
- `WebSocket /ws` - Real-time state streaming

### Cross-System Communication (Port 8006)
Dedicated WebSocket server for secure cross-system messaging between consciousness and AGI systems.

## OpenAPI Documentation

Interactive API documentation is available at:
- http://localhost:8003/docs - Main API documentation
- http://localhost:8005/docs - Unified API documentation

These documentation interfaces are automatically generated from the OpenAPI specifications and provide:
- Interactive endpoint testing
- Request/response examples
- Schema definitions
- Authentication information

## Using OpenAPI with AEGIS

### Accessing the API

To access the AEGIS API, you can use any HTTP client. Here's a simple example using curl:

```bash
# Get consciousness state
curl http://localhost:8003/api/consciousness

# Send chat message
curl -X POST http://localhost:8003/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello AEGIS!", "session_id": "session123"}'
```

### WebSocket Integration

For real-time updates, connect to the WebSocket endpoint:

```javascript
const ws = new WebSocket('ws://localhost:8006/ws');

ws.onopen = function(event) {
    console.log('Connected to AEGIS WebSocket');
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};
```

## OpenAPI Specification Files

Machine-readable OpenAPI specifications are available at:
- http://localhost:8003/openapi.json
- http://localhost:8005/openapi.json

These JSON files can be used with OpenAPI tools for:
- Client code generation
- API testing
- Documentation generation
- Validation

## Security Considerations

When using the AEGIS OpenAPI interfaces, consider the following security aspects:

1. **Authentication**: In production environments, API endpoints may require authentication tokens
2. **Encryption**: All communication should be encrypted using HTTPS/TLS
3. **Rate Limiting**: Be aware of rate limits to prevent overwhelming the system
4. **Input Validation**: Always validate input data to prevent injection attacks

## OpenAPI Tools Integration

AEGIS's OpenAPI specification can be used with various tools:

### Code Generation
Generate client libraries in various programming languages:
```bash
# Using openapi-generator
openapi-generator generate -i http://localhost:8003/openapi.json -g python -o ./client
```

### API Testing
Import the specification into testing tools like Postman or Insomnia for automated testing.

### Documentation Generation
Use tools like ReDoc or Swagger UI to generate standalone documentation.

## Best Practices

When working with AEGIS's OpenAPI:

1. **Always check the health endpoint** first to ensure the system is running
2. **Handle errors gracefully** by checking HTTP status codes
3. **Use appropriate headers** for content type and authentication
4. **Implement retry logic** for transient failures
5. **Monitor rate limits** to avoid being throttled

## Extending the API

For developers looking to extend AEGIS functionality:

1. Follow the existing OpenAPI specification patterns
2. Maintain consistent naming conventions
3. Provide comprehensive documentation for new endpoints
4. Implement proper error handling and status codes
5. Ensure backward compatibility when possible

## Troubleshooting

Common issues and solutions:

1. **Connection Refused**: Ensure AEGIS is running and the correct port is being used
2. **404 Not Found**: Check that the endpoint URL is correct
3. **400 Bad Request**: Validate that request parameters and body are correctly formatted
4. **500 Internal Server Error**: Check system logs for detailed error information

For more detailed information about AEGIS's API implementation, see the [API Integration](API_INTEGRATION) documentation.