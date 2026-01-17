# How to Run Onyx on Android (via Termux)

This guide explains how to transfer the Onyx files to your Android device and run them using Termux.

## Prerequisites
1.  **Termux App**: Install from F-Droid (recommended) or GitHub. *Do not use the Play Store version as it is outdated.*
2.  **Onyx Files**: You need the `Onyx` folder from this computer.

## Step 1: Transfer Files to Phone

Choose **ONE** of the following methods to get the `Onyx` folder onto your phone.

### Method A: Wired (USB)
1.  Connect your phone to your PC via USB.
2.  Select "File Transfer" mode on your phone.
3.  Copy the `Onyx` folder to your phone's internal storage (e.g., inside `Downloads`).
4.  Open Termux on your phone.
5.  Run this command to grant storage access:
    ```bash
    termux-setup-storage
    ```
6.  Copy the folder from storage to Termux home:
    ```bash
    cp -r /sdcard/Download/Onyx ~/Onyx
    ```

### Method B: Wireless (Python Server)
1.  On your PC (in the directory containing the `Onyx` folder), run:
    ```bash
    # Run this in the parent directory of 'Onyx'
    python3 -m http.server 8000
    ```
2.  Find your PC's local IP address (e.g., `192.168.1.X`).
3.  Open Termux on your phone.
4.  Install wget: `pkg install wget`
5.  Download the files recursively (wget can be tricky for folders, zip is better).
    *   **Better way**: Zip the folder on PC first:
        ```bash
        # On PC
        zip -r onyx.zip Onyx/
        ```
    *   **On Termux**:
        ```bash
        wget http://YOUR_PC_IP:8000/onyx.zip
        unzip onyx.zip
        ```

## Step 2: Setup Onyx

Once you have the `Onyx` folder inside Termux:

1.  Enter the directory:
    ```bash
    cd ~/Onyx
    ```
2.  Make the setup script executable:
    ```bash
    chmod +x setup_termux.sh
    ```
3.  Run the setup script (this will take a while!):
    ```bash
    ./setup_termux.sh
    ```

## Step 3: Run Onyx

After setup completes successfully:

1.  Activate the environment:
    ```bash
    source venv/bin/activate
    ```
2.  Run the app:
    ```bash
    python main.py
    ```

## Troubleshooting
*   **"Killed"**: If the app crashes with "Killed" while loading a model, your phone ran out of RAM. Try a smaller model (like a 3B parameter model).
*   **"Illegal Instruction"**: The model or library is compiled for a different architecture. You may need to compile `gpt4all` manually (see setup script output).
