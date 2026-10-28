# FP Gemini Edition 1

A modular Python chatbot starter with feature toggles for multimodal tools, chat persistence, and session resume.

## Included capabilities

- terminal chat interface
- session save/load support
- app-level chat history persistence
- JSON-controlled tool enablement
- TTS support
- STT support
- image generation
- image reading
- web search
- voice cloning
- calculator
- file editing helpers
- external API hooks

## Feature config

The feature list is controlled by `config/features.json`.

Example:

```json
{
  "enabled_tools": {
    "tts": true,
    "stt": true,
    "image_gen": true,
    "image_read": true,
    "web_search": true
  }
}
```

Set any tool to `false` to disable it.

## Run the app

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Commands

- `resume` to continue your last session
- `help` for command hints
- `exit` or `quit` to leave

## Session persistence

The app saves session data to `data/sessions/` and chat history to `data/chat_history.jsonl`.
