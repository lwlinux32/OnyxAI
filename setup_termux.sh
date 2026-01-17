#!/data/data/com.termux/files/usr/bin/bash

# Termux Setup Script for Onyx
# This script installs necessary dependencies and sets up the Python environment.

echo ">>> Starting Onyx Setup for Termux..."

# 1. Update Termux repositories
echo ">>> Updating Termux packages..."
pkg update -y && pkg upgrade -y

# 2. Install System Dependencies
echo ">>> Installing system dependencies..."
# clang/cmake/build-essential for compiling bindings
# python for the runtime
# git to clone repos if needed
pkg install python clang cmake git build-essential binutils rust -y

# 3. Virtual Environment Setup
echo ">>> Setting up Python Virtual Environment..."
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "    Created 'venv'."
else
    echo "    'venv' already exists."
fi

# Activate venv
source venv/bin/activate

# 4. Install Dependencies
echo ">>> Installing Python dependencies..."

# Upgrade pip
pip install --upgrade pip

# Install basic requirements first
echo "    Installing rich, pyyaml, requests..."
pip install rich pyyaml requests

# 5. Handle GPT4All (The tricky part on ARM)
echo ">>> Attempting to install GPT4All..."

# Try standard install first (might work on some Termux setups now)
if pip install gpt4all; then
    echo ">>> GPT4All installed successfully via pip!"
else
    echo ">>> Standard pip install failed (expected on ARM)."
    echo ">>> Attempting to build from source or find compatible wheel..."
    
    # NOTE: As of 2026, GPT4All python bindings on Termux often require manual build.
    # We will try a fallback strategy using a known compatible method or instructing the user.
    
    echo "!!! CRITICAL: Automatic installation of GPT4All failed."
    echo "!!! You may need to build the python bindings manually."
    echo "!!! Detailed instructions:"
    echo "1. Clone the gpt4all repo: git clone --recurse-submodules https://github.com/nomic-ai/gpt4all"
    echo "2. Navigate to gpt4all-backend and build using cmake."
    echo "3. Navigate to gpt4all-python and pip install ."
    echo "For now, we will proceed, but the app might fail if 'import gpt4all' doesn't work."
fi

echo ">>> Setup Complete!"
echo "To start Onyx:"
echo "1. source venv/bin/activate"
echo "2. python main.py"
