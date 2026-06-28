# SageWire STT Service

Standalone Speech-to-Text infrastructure service for SageWire applications.

## Endpoints

### Health

GET /health

### Transcribe

POST /transcribe

Form field:

audio

Returns:

```json
{
  "text": "spoken words here",
  "language": "en",
  "duration": 3.4
}
