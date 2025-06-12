# Massive Rocket Braze CRM Backend Prototype

## Overview

This prototype demonstrates a backend system designed to improve reliability and scalability for Braze CRM campaign orchestration. It includes:

- Template validation service for Liquid templates
- Event deduplication using Redis TTL cache
- Braze API client with retry and backoff logic
- Simple FastAPI endpoints for validation and event sending

## Setup

1. Install Redis and run it locally or use a Redis server.
2. Create a Python virtual environment and install dependencies:

```
pip install -r requirements.txt
```

3. Run the FastAPI server:

```
uvicorn app.main:app --reload
```

## Endpoints

- `POST /validate-template/`  
  Validates a Liquid template against sample payloads.

- `POST /send-event/`  
  Sends an event to Braze with deduplication and retry logic.

## Example Requests

### Validate Template

```json
POST /validate-template/
{
  "template": "Hello {{ user.name }}",
  "payloads": [{"user": {"name": "Dee"}}, {"user": {}}]
}
```

### Send Event

```json
POST /send-event/
{
  "event_id": "event-123",
  "payload": {
    "audience": {...},
    "messages": {...}
  }
}
```

## Testing

Run tests with:

```
pytest
```

## Notes

- Update `your_braze_api_key_here` in `braze_client.py` with your Braze API key.
- This prototype can be extended with MJML validation, campaign orchestration, and metrics.