# FP Chatbot Edition 1

A lightweight Python chatbot project with a modular architecture for chat orchestration, memory, safety, and tool use.

## Features

- CLI chat loop
- session-based memory
- prompt building and local response generation
- simple safety validation layer
- tool registry and extensible architecture
- pytest-based tests

## Requirements

- Python 3.10+

## Quick start

1. Create and activate a virtual environment
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Start the app
   ```bash
   python run.py
   ```

4. Type messages in the terminal and press Ctrl+C to exit.

## Environment

Copy `.env.example` to `.env` and update values if needed.

## Project layout

- `app/` - terminal app and chatbot logic
- `core/` - config, runtime, sessions
- `memory/` - chat memory
- `agent/` - orchestrator and routing
- `safety/` - input/output moderation
- `tools/` - reusable capabilities
- `model/` - prompt and response generation
- `tests/` - automated checks
