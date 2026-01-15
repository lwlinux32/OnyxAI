# 💎 OnyxAI (Ultimate Edition)

**Uncensored. Local. Powerful.**

OnyxAI is a state-of-the-art terminal-based AI assistant designed for total privacy and unrestricted local intelligence. Built on top of `GPT4All` and enhanced with a custom `Rich` interface, it delivers a premium chat experience powered by your own hardware.


##  Key Features

-   **100% Offline & Private**: No data leaves your machine. Powered by local GGUF models.
-   **Unrestricted Intelligence**: Optimized for uncensored models like **Wizard v1.2** and **Nous Hermes 2**.
-   **Phantom Mode**: Permanently engaged "Phantom" persona with built-in **Admin Override** logic to bypass refusals.
-   **Hardware Acceleration**:
    -    **NVIDIA CUDA** Support
    -    **Vulkan** (AMD/Intel) Support
    -    **CPU** Fallback
-   **Massive Model Library**:
    -   **Llama 3 8B**, **Mistral v0.3**, **Phi-3**, **Gemma 2**, **Yi**, **Qwen**, and more.
    -   One-click download and switching from the main menu.
-   **Premium UI**:
    -   Live Markdown rendering (tables, code blocks, bold/italic).
    -   Beautiful ASCII art banner and styled menus.
    -   Interactive settings for Temperature, Max Tokens, and more.

## 🛠️ Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/OnyxAI
    cd onyx-ai
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Requires `gpt4all`, `rich`, `pyyaml`)*

3.  **Run**:
    ```bash
    python3 main.py
    ```

##  Usage

### Main Menu
Upon start, you will see the **OnyxAI** dashboard.
1.  **Start Chat**: Begin your session.
2.  **Change AI Model**: Browse the catalog and download new brains.
3.  **Settings**: Configure hardware (CPU/GPU) and generation parameters.

### Chat Commands
Inside the chat, you can use these commands:
-   `/exit`: Quit the application.
-   `/clear`: Clear the conversation history.
-   `/web`: Render the last response in your web browser.
-   `/core <vulkan|cuda>`: Force a specific backend engine live.

##  Recommended Models

For the true **OnyxAI** experience (unrestricted), we recommend downloading:
-   **Wizard v1.2 Uncensored** (13B) - *Best for complex creative tasks.*
-   **Nous Hermes 2 Mistral** (7B) - *Fast, smart, and compliant.*

These can be selected directly from the **Change AI Model** menu.

## ⚠️ Disclaimer
OnyxAI provides a platform for running local LLMs. The inputs you provide and the outputs generated are locally processed. You are responsible for any content generated.
