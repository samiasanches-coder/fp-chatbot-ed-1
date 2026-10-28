# FP Gemini Edition 1

A modular Python chatbot starter with a feature-toggle system for multi-modal tools.

## Included capabilities

- chat conversation with session resume
- conversation history saved to file
- JSON-driven feature enablement
- TTS support
- STT support
- image generation
- image reading
- web search
- voice cloning
- calculator
- file editing helpers
- external API hooks

## Features config

The feature list is controlled in `config/features.json`.

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

Then ask things like:
- create a voice with a specific tone
- generate an image of a cyberpunk city
- read an image file
- search the web for AI news
- transcribe audio
- calculate a math expression

## Session persistence

The app saves session data to `data/sessions/` and chat history to `data/chat_history.jsonl`.
Type `resume` in the CLI to continue the most recent session.

## Architecture

This project is structured so the interface, session management, tool registry, and feature toggles are separated into independent modules.
