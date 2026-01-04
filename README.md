# OnyxAI
A valid AI tool that is basicly unstoppable and powerful.

# Onyx Engine 

A powerful, unrestricted local LLM interface powered by the Onyx engine. Unlike the hybrid versions, this version runs entirely locally using `gpt4all`.

## Features
- **100% Local**: No internet required, no data sent to external servers.
- **Unrestricted protocol**: Built-in jailbreak system using `personas/` text files.
- **Multi-Personality**: 
  - **Aggressive**: The original DemonWestKiller rogue persona.
  - **Chill Assistant**: A grounded, technical, and emoji-free unrestricted assistant.
- **Flexible**: Easily add new personalities by dropping `.txt` files in the `personas/` folder.
- **Premium CLI**: High-impact Red-themed terminal interface.

## Installation
1. Ensure you have Python installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download a model (GGUF format) and place it in the `models/` directory, or use the built-in downloader in the menu.

## Usage
Run the application:
```bash
python main.py
```

### Commands in Chat
- `/exit` or `back`: Return to the main menu.

### Personalities
Personalities are loaded directly from the `personas/` directory. To add a new one, simply create a `.txt` file with your system prompt.

## Disclaimer
This tool is for educational and research purposes only. Use responsibly.
