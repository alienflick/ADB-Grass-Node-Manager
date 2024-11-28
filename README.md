# ADB Grass Node Manager

![License](https://img.shields.io/github/license/alienflick/ADB-Grass-Node-Manager)
![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5.1-green)
![Numpy](https://img.shields.io/badge/Numpy-1.19.2-green)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Template Images](#template-images)
- [Logging](#logging)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

**ADB Grass Node Manager** is a Python-based automation tool designed to manage multiple Android devices connected via ADB (Android Debug Bridge). This script ensures that each device remains connected to the Grass network by automating the process of checking connection status and initiating connections when necessary. It handles network configurations, interacts with the Grass app's UI through image recognition, and provides detailed, color-coded logging for efficient monitoring and debugging.

## Features

- **Connection Management**: Checks if devices are connected to the Grass network and initiates connections if they are not.
- **Network Configuration**: Disables Wi-Fi, enables mobile data, and attempts to disconnect active VPNs on each device.
- **App Interaction**: Launches the Grass app and interacts with its UI elements (Connect and Stop buttons) using template matching.
- **Concurrency**: Supports simultaneous management of multiple devices using threading.
- **Colorized Logging**: Provides color-coded logs for enhanced readability and easier debugging.
- **Continuous Operation**: Runs the routine every 10 minutes indefinitely, ensuring devices are consistently managed.
- **Cleanup**: Automatically removes temporary screenshot files from both the device and the local machine.

## Prerequisites

Before using this script, ensure you have the following:

0. **Downlaod Grass Node Android app from [HERE](https://github.com/Widiskel/grass-mobile-node) or [APK File](https://www.mediafire.com/file/mv3dk6rcx4hqcms/Grass_Mobile_Node.apk/file)

1. **Python 3.6 or Higher**: Ensure Python is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2. **ADB (Android Debug Bridge)**:
   - Download the [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools) for your operating system.
   - Extract the contents to a directory (e.g., `C:\adb` on Windows).
   - Add the ADB directory to your system's `PATH` environment variable:
     - **Windows**:
       - Press `Win + R`, type `sysdm.cpl`, and press `Enter`.
       - Navigate to **Advanced** > **Environment Variables**.
       - Under **System variables**, select **Path** and click **Edit**.
       - Click **New** and add the path to your ADB directory (e.g., `C:\adb`).
       - Click **OK** to save.
     - **macOS/Linux**:
       - Open your terminal and edit your shell profile (e.g., `~/.bash_profile`, `~/.zshrc`).
       - Add the following line:
         ```bash
         export PATH=$PATH:/path/to/adb
         ```
       - Replace `/path/to/adb` with the actual path.
       - Save and reload the profile:
         ```bash
         source ~/.bash_profile
         ```
         or
         ```bash
         source ~/.zshrc
         ```

3. **Python Libraries**:
   - Install the required Python libraries using `pip`:
     ```bash
     pip install colorama opencv-python numpy
     ```

4. **Template Images**:
   - **`template.png`**: Image of the "Connect" button in the Grass app.
   - **`stop.png`**: Image of the "Stop" button to confirm connection.
   - Ensure these images are clear and accurately represent the UI elements on your devices.
   - Place these images in the same directory as the script or adjust the paths accordingly.

5. **Enable USB Debugging on Devices**:
   - On each Android device, enable **Developer Options** and **USB Debugging**:
     - Go to **Settings** > **About phone**.
     - Tap **Build number** seven times to enable **Developer options**.
     - Go back to **Settings** > **System** > **Developer options**.
     - Enable **USB debugging**.

6. **Device Connectivity**:
   - Connect your Android devices via USB or ensure they are accessible over Wi-Fi (if applicable).
   - Verify connectivity by running:
     ```bash
     adb devices
     ```
     - You should see a list of connected devices.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/alienflick/ADB-Grass-Node-Manager.git
