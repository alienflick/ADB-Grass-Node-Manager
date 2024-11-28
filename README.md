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

0. **Download Grass Node Android** app from [HERE](https://github.com/Widiskel/grass-mobile-node) or [APK File](https://www.mediafire.com/file/mv3dk6rcx4hqcms/Grass_Mobile_Node.apk/file)

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
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd ADB-Grass-Node-Manager
   ```

3. **Install the Required Python Libraries** (if not already installed):
   ```bash
   pip install colorama opencv-python numpy
   ```

## Configuration

1. **Edit the Configuration File**:
   - Open the `config.json` file to modify any configurations, such as interval times or image paths.
   - Ensure that the device serial numbers match those connected via ADB for proper management.

## Usage

1. **Run the Script**:
   - Execute the script by running:
     ```bash
     python main.py
     ```
   - The script will start monitoring and managing the connected devices, performing checks and taking necessary actions every 10 minutes.

2. **Logs and Output**:
   - The script will display logs on the terminal indicating the status of each device and any actions taken.
   - The logs are color-coded to enhance readability, with different colors for informational messages, warnings, and errors.

## Template Images

- **Template Matching**: The script uses OpenCV's template matching feature to identify specific buttons in the Grass app.
- Ensure that:
  - The images (`template.png` and `stop.png`) are clear and accurately represent the buttons on your device screens.
  - They are placed in the same directory as the script or the correct paths are provided in the script.

## Logging

- **Colorized Logs**: The script uses the `colorama` library to provide color-coded logs:
  - **Info**: General information about the script's actions.
  - **Warning**: Issues that may need attention (e.g., unable to locate a button).
  - **Error**: Critical issues that stop the script from functioning properly.
- The logs are printed in the terminal and help in monitoring the progress and debugging any issues.

## Troubleshooting

1. **ADB Not Recognized**: Ensure that ADB is installed correctly and that its path is added to the system's `PATH` variable.
2. **Device Not Found**: Make sure the device is connected properly and USB Debugging is enabled.
3. **Template Matching Fails**: Verify that the template images are accurate and have sufficient clarity.
4. **Permission Issues**: Ensure that your Python script has the necessary permissions to access ADB and device storage.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features you would like to add.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

