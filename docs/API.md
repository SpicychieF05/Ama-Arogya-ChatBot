# API Documentation

## Authentication
Currently, the API does not require authentication, but this can be easily added for production use.

## Base URL
```
http://localhost:8001
```

## Endpoints

### Health Check
```http
GET /health
```
Returns the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1640995200.0,
  "version": "2.0.0",
  "rasa_enabled": false,
  "cache_size": 25
}
```

### Chat Endpoint
```http
POST /chat
```
Send a message to the chatbot and receive a response.

**Request Body:**
```json
{
  "message": "I have a fever",
  "sender_id": "user123",
  "language": "en"
}
```

**Response:**
```json
{
  "response": "For fever: Take adequate rest, stay hydrated...",
  "language": "en",
  "intent": "fever_management",
  "response_time_ms": 45.2,
  "source": "fallback"
}
```

### Statistics
```http
GET /stats
```
Get usage statistics and analytics.

**Response:**
```json
{
  "total_interactions": 1523,
  "language_distribution": {
    "en": 856,
    "hi": 425,
    "or": 242
  },
  "popular_topics": [
    {
      "intent": "fever_management",
      "count": 145,
      "avg_response_time": 42.3
    }
  ],
  "response_time_avg": 38.7
}
```

### Admin Endpoints

#### Clear Cache
```http
POST /admin/cache/clear
```
Clear the response cache (admin only).

## Error Handling
All endpoints return appropriate HTTP status codes:
- `200` - Success
- `400` - Bad Request (invalid input)
- `404` - Not Found
- `500` - Internal Server Error

## Rate Limiting
The API supports up to 100 concurrent requests by default. This can be configured in the environment settings.