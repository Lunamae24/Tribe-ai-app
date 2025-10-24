# API Documentation

## Base URL

Production: `https://yourdomain.com`  
Development: `http://localhost:8000`

## Authentication

Most endpoints require authentication using API keys or JWT tokens.

### API Key Authentication

Include your API key in the request header:

```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### Health & Status

#### GET /health

Basic health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000000"
}
```

#### GET /health/detailed

Detailed health check with system metrics.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000000",
  "system": {
    "cpu_percent": 25.5,
    "memory_percent": 45.2,
    "disk_percent": 60.0,
    "python_version": "3.11.0"
  },
  "checks": {
    "database": "ok",
    "redis": "ok"
  }
}
```

#### GET /health/ready

Kubernetes readiness probe.

**Response:**
```json
{
  "status": "ready"
}
```

#### GET /health/live

Kubernetes liveness probe.

**Response:**
```json
{
  "status": "alive"
}
```

### AI Endpoints

#### POST /api/v1/ai/chat

Chat with AI models.

**Request:**
```json
{
  "message": "Hello, how are you?",
  "model": "gpt-4",
  "temperature": 0.7,
  "max_tokens": 2000
}
```

**Parameters:**
- `message` (required): The message to send to the AI
- `model` (optional): AI model to use (default: from config)
- `temperature` (optional): Response randomness 0-1 (default: 0.7)
- `max_tokens` (optional): Maximum tokens in response (default: 2000)

**Response:**
```json
{
  "response": "Hello! I'm doing well, thank you for asking...",
  "model": "gpt-4",
  "tokens_used": 150
}
```

**Status Codes:**
- `200 OK`: Success
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Authentication required
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

#### GET /api/v1/ai/models

List available AI models.

**Response:**
```json
{
  "models": [
    "gpt-4",
    "gpt-3.5-turbo",
    "claude-3-opus",
    "claude-3-sonnet"
  ]
}
```

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message description"
}
```

### Common Error Codes

- `400 Bad Request`: Invalid input parameters
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Service temporarily unavailable

## Rate Limiting

API endpoints are rate-limited to prevent abuse:

- **Per Minute**: 60 requests
- **Per Hour**: 1000 requests

When rate limit is exceeded, you'll receive a `429 Too Many Requests` response:

```json
{
  "detail": "Rate limit exceeded. Please try again later."
}
```

## Versioning

The API uses URL versioning. Current version is `v1`.

Example: `/api/v1/ai/chat`

## CORS

CORS is configured to allow requests from specified origins. For production, only your domain(s) will be allowed.

## Examples

### cURL

```bash
# Health check
curl https://yourdomain.com/health

# Chat request
curl -X POST https://yourdomain.com/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "message": "What is AI?",
    "model": "gpt-4"
  }'
```

### Python

```python
import requests

# Health check
response = requests.get("https://yourdomain.com/health")
print(response.json())

# Chat request
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
data = {
    "message": "What is AI?",
    "model": "gpt-4"
}
response = requests.post(
    "https://yourdomain.com/api/v1/ai/chat",
    headers=headers,
    json=data
)
print(response.json())
```

### JavaScript

```javascript
// Health check
fetch('https://yourdomain.com/health')
  .then(response => response.json())
  .then(data => console.log(data));

// Chat request
fetch('https://yourdomain.com/api/v1/ai/chat', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: 'What is AI?',
    model: 'gpt-4'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Best Practices

1. **Always use HTTPS** in production
2. **Store API keys securely** (never in code)
3. **Implement retry logic** for transient failures
4. **Handle rate limits** gracefully
5. **Validate responses** before using data
6. **Use appropriate timeouts** for requests
7. **Log errors** for debugging

## Support

For API support, please:
1. Check this documentation
2. Review error messages
3. Open a GitHub issue
4. Contact support team

## Changelog

### Version 1.0.0 (Current)
- Initial release
- Health check endpoints
- AI chat endpoint
- Model listing endpoint
