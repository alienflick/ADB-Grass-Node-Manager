import subprocess
import cv2
import numpy as np
import os
import time
import threading
import re
import datetime
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Define paths for the template images
template_path = 'template.png'  # The "Connect" button image
stop_template_path = 'stop.png'  # The "Stop" button image to confirm connection

# App package name
app_package = 'com.wskel.grass'

# Log level colors
LOG_LEVELS = {
    'INFO': Fore.CYAN,
    'DEBUG': Fore.BLUE,
    'WARNING': Fore.YELLOW,
    'ERROR': Fore.RED
}

# Custom logging function
def log(message, level='INFO', device_id=None):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    color = LOG_LEVELS.get(level, Fore.WHITE)
    device_str = f"[{device_id}]" if device_id else ""
    formatted_message = f"{color}{timestamp} {device_str} [{level}] {message}{Style.RESET_ALL}"
    print(formatted_message)

# Set the working directory to the script's location
def set_working_directory():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    log(f"Working directory set to: {script_dir}", level='DEBUG')

# Function to get list of connected devices
def get_connected_devices():
    log("Retrieving list of connected devices...", level='INFO')
    result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    devices_output = result.stdout.strip().splitlines()
    devices = []
    for line in devices_output[1:]:
        if line.strip():
            parts = line.split()
            if len(parts) >= 2 and parts[1] == 'device':
                devices.append(parts[0])
    log(f"Connected devices: {devices}", level='INFO')
    return devices

# Function to perform actions on a single device
def process_device(device_id):
    log("Starting processing of device.", level='INFO', device_id=device_id)
    screenshot_device_path = f'/sdcard/screenshot_{device_id}.png'
    screenshot_local_path = f'screenshot_{device_id}.png'

    # Unlock the device if locked or screen is off
    def unlock_device():
        log("Unlocking the device...", level='INFO', device_id=device_id)
        # Wake up the device
        subprocess.run(['adb', '-s', device_id, 'shell', 'input', 'keyevent', 'KEYCODE_WAKEUP'])
        # Dismiss the keyguard if any
        subprocess.run(['adb', '-s', device_id, 'shell', 'wm', 'dismiss-keyguard'])
        # Simulate swipe up to unlock (adjust coordinates if necessary)
        subprocess.run(['adb', '-s', device_id, 'shell', 'input', 'swipe', '300', '1000', '300', '500', '500'])
        time.sleep(1)  # Wait for the device to unlock

    # Open the app
    def open_app():
        log(f"Opening the app '{app_package}'...", level='INFO', device_id=device_id)
        # Launch the app
        subprocess.run(['adb', '-s', device_id, 'shell', 'monkey', '-p', app_package, '-c', 'android.intent.category.LAUNCHER', '1'])
        time.sleep(5)  # Wait for the app to open

    # Disconnect VPN, disable Wi-Fi, and enable mobile data
    def manage_network_connections():
        log("Managing network connections...", level='INFO', device_id=device_id)
        # Disable Wi-Fi
        subprocess.run(['adb', '-s', device_id, 'shell', 'svc', 'wifi', 'disable'])
        # Enable mobile data
        subprocess.run(['adb', '-s', device_id, 'shell', 'svc', 'data', 'enable'])
        # Attempt to disconnect VPN (requires Android 7.0 or higher)
        # List active VPNs
        vpn_list = subprocess.run(['adb', '-s', device_id, 'shell', 'dumpsys', 'vpn'], stdout=subprocess.PIPE, text=True).stdout
        if 'VPN is up' in vpn_list:
            log("VPN is active. Attempting to disconnect...", level='INFO', device_id=device_id)
            # This is a placeholder. Disconnecting VPN via ADB is limited and may require specific commands
            # For known VPN apps, you can force-stop them
            vpn_apps = ['com.example.vpnapp1', 'com.example.vpnapp2']  # Replace with actual VPN app package names
            for vpn_app in vpn_apps:
                subprocess.run(['adb', '-s', device_id, 'shell', 'am', 'force-stop', vpn_app])
        else:
            log("No active VPN detected.", level='INFO', device_id=device_id)
        time.sleep(2)  # Wait for network changes to take effect

    # Capture the screen of the Android device
    def capture_screenshot():
        log("Capturing screenshot on the device...", level='DEBUG', device_id=device_id)
        subprocess.run(['adb', '-s', device_id, 'shell', 'screencap', '-p', screenshot_device_path])

    # Pull the screenshot to your local machine
    def pull_screenshot():
        log("Pulling screenshot to local machine...", level='DEBUG', device_id=device_id)
        subprocess.run(['adb', '-s', device_id, 'pull', screenshot_device_path, screenshot_local_path])

    # Read images using OpenCV
    def read_images():
        log("Reading images...", level='DEBUG', device_id=device_id)
        log(f"Screenshot path: {screenshot_local_path}", level='DEBUG', device_id=device_id)
        log(f"Template image path: {template_path}", level='DEBUG', device_id=device_id)
        log(f"Stop template image path: {stop_template_path}", level='DEBUG', device_id=device_id)

        if not os.path.exists(screenshot_local_path):
            log(f"Screenshot not found at {screenshot_local_path}. Exiting.", level='ERROR', device_id=device_id)
            return None, None, None

        if not os.path.exists(template_path):
            log(f"Template image not found at {template_path}. Exiting.", level='ERROR', device_id=device_id)
            return None, None, None

        if not os.path.exists(stop_template_path):
            log(f"Stop template image not found at {stop_template_path}. Exiting.", level='ERROR', device_id=device_id)
            return None, None, None

        screenshot = cv2.imread(screenshot_local_path, cv2.IMREAD_COLOR)
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        stop_template = cv2.imread(stop_template_path, cv2.IMREAD_COLOR)

        if screenshot is None:
            log("Failed to read screenshot. Exiting.", level='ERROR', device_id=device_id)
            return None, None, None
        if template is None:
            log("Failed to read template image. Exiting.", level='ERROR', device_id=device_id)
            return None, None, None
        if stop_template is None:
            log("Failed to read stop template image. Exiting.", level='ERROR', device_id=device_id)
            return None, None, None
        return screenshot, template, stop_template

    # Calculate dynamic scale range based on device and template dimensions
    def calculate_scale_range(screenshot_dimensions, template_dimensions):
        screenshot_width, screenshot_height = screenshot_dimensions
        template_width, template_height = template_dimensions
        scale_x = screenshot_width / template_width
        scale_y = screenshot_height / template_height
        min_scale = min(scale_x, scale_y) * 0.5
        max_scale = max(scale_x, scale_y) * 1.5
        scales = np.linspace(min_scale, max_scale, 30)  # Adjust number of scales as needed
        return scales

    # Perform multi-scale template matching with dynamic scales
    def find_template_multiscale(screenshot, template):
        gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # Calculate scales based on device and template dimensions
        scales = calculate_scale_range(
            (screenshot.shape[1], screenshot.shape[0]),
            (template.shape[1], template.shape[0])
        )

        found = None
        for scale in scales:
            resized_template = cv2.resize(gray_template, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            w, h = resized_template.shape[::-1]
            if w > gray_screenshot.shape[1] or h > gray_screenshot.shape[0]:
                continue

            result = cv2.matchTemplate(gray_screenshot, resized_template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.7  # Adjusted threshold
            loc = np.where(result >= threshold)
            if len(loc[0]) > 0:
                max_val = result[loc].max()
                max_loc = np.unravel_index(result.argmax(), result.shape)
                # Log matching details for debugging
                log(f"Match found at scale {scale:.2f} with value {max_val:.2f}", level='DEBUG', device_id=device_id)
                if found is None or max_val > found[0]:
                    found = (max_val, max_loc, scale, w, h)
        if found:
            _, max_loc, scale, w, h = found
            x, y = max_loc[1], max_loc[0]
            return x, y, w, h
        else:
            return None

    # Get device screen dimensions
    def get_device_screen_dimensions():
        result = subprocess.run(['adb', '-s', device_id, 'shell', 'wm', 'size'], stdout=subprocess.PIPE, text=True)
        size_output = result.stdout.strip()
        match = re.search(r'Physical size: (\d+)x(\d+)', size_output)
        if match:
            width, height = int(match.group(1)), int(match.group(2))
            log(f"Screen dimensions: width={width}, height={height}", level='DEBUG', device_id=device_id)
            return width, height
        else:
            log("Unable to get screen dimensions.", level='ERROR', device_id=device_id)
            return None, None

    # Adjust tap coordinates based on screen scaling
    def adjust_tap_coordinates(x, y, screenshot_dimensions, screen_dimensions):
        screenshot_width, screenshot_height = screenshot_dimensions
        screen_width, screen_height = screen_dimensions
        scale_x = screen_width / screenshot_width
        scale_y = screen_height / screenshot_height
        adjusted_x = int(x * scale_x)
        adjusted_y = int(y * scale_y)
        log(f"Adjusted tap coordinates: x={adjusted_x}, y={adjusted_y}", level='DEBUG', device_id=device_id)
        return adjusted_x, adjusted_y

    # Perform a tap action at the detected coordinates
    def tap_on_device(x, y):
        log(f"Tapping on the device at coordinates: x={x}, y={y}", level='INFO', device_id=device_id)
        result = subprocess.run(
            ['adb', '-s', device_id, 'shell', 'input', 'tap', str(int(x)), str(int(y))],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            log(f"Error executing tap command: {result.stderr}", level='ERROR', device_id=device_id)
        else:
            log("Tap command executed successfully.", level='INFO', device_id=device_id)

    # Press the home button to minimize the app
    def press_home_button():
        log("Pressing the home button to minimize the app.", level='INFO', device_id=device_id)
        result = subprocess.run(
            ['adb', '-s', device_id, 'shell', 'input', 'keyevent', 'KEYCODE_HOME'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            log(f"Error pressing home button: {result.stderr}", level='ERROR', device_id=device_id)
        else:
            log("Home button pressed successfully.", level='INFO', device_id=device_id)

    # Wait for up to specified time to confirm the image is no longer on the screen
    def wait_for_image_to_disappear(template, timeout=60, check_interval=5):
        log("Waiting for the image to disappear...", level='INFO', device_id=device_id)
        start_time = time.time()
        while time.time() - start_time < timeout:
            capture_screenshot()
            time.sleep(1)  # Ensure the screenshot is saved
            pull_screenshot()
            screenshot = cv2.imread(screenshot_local_path, cv2.IMREAD_COLOR)
            if screenshot is None:
                log("Failed to read screenshot during waiting period.", level='ERROR', device_id=device_id)
                return False
            match = find_template_multiscale(screenshot, template)
            if match is None:
                log("Image is no longer found on the screen.", level='INFO', device_id=device_id)
                return True
            else:
                log("Image still present on the screen. Checking again in a few seconds...", level='DEBUG', device_id=device_id)
                time.sleep(check_interval)
        log("Timeout reached. Image is still on the screen.", level='WARNING', device_id=device_id)
        return False

    # Wait for up to specified time to confirm the image appears on the screen
    def wait_for_image_to_appear(template, timeout=30, check_interval=5):
        log("Waiting for the image to appear...", level='INFO', device_id=device_id)
        start_time = time.time()
        while time.time() - start_time < timeout:
            capture_screenshot()
            time.sleep(1)  # Ensure the screenshot is saved
            pull_screenshot()
            screenshot = cv2.imread(screenshot_local_path, cv2.IMREAD_COLOR)
            if screenshot is None:
                log("Failed to read screenshot during waiting period.", level='ERROR', device_id=device_id)
                return False
            match = find_template_multiscale(screenshot, template)
            if match:
                log("Image appeared on the screen.", level='INFO', device_id=device_id)
                return True
            else:
                log("Image not present yet. Checking again in a few seconds...", level='DEBUG', device_id=device_id)
                time.sleep(check_interval)
        log("Timeout reached. Image did not appear on the screen.", level='WARNING', device_id=device_id)
        return False

    # Cleanup function to remove the screenshot from the device and local machine
    def cleanup():
        log("Cleaning up...", level='INFO', device_id=device_id)
        subprocess.run(['adb', '-s', device_id, 'shell', 'rm', screenshot_device_path])
        if os.path.exists(screenshot_local_path):
            os.remove(screenshot_local_path)

    # Main logic for the device
    unlock_device()
    manage_network_connections()
    open_app()
    time.sleep(2)  # Wait for app to settle
    capture_screenshot()
    time.sleep(1)  # Wait to ensure the screenshot is saved
    pull_screenshot()
    screenshot, template, stop_template = read_images()
    if screenshot is None or template is None or stop_template is None:
        cleanup()
        return

    # Get device and screenshot dimensions
    screen_width, screen_height = get_device_screen_dimensions()
    if screen_width is None or screen_height is None:
        cleanup()
        return
    screenshot_height, screenshot_width = screenshot.shape[:2]
    log(f"Screenshot dimensions: width={screenshot_width}, height={screenshot_height}", level='DEBUG', device_id=device_id)

    # Check if the device is already connected (stop.png exists)
    stop_match = find_template_multiscale(screenshot, stop_template)
    if stop_match:
        log("Device is already connected. Skipping tap action.", level='INFO', device_id=device_id)
        cleanup()
        # Press the home button to minimize the app
        press_home_button()
        return

    # Attempt to find and tap the "Connect" button (template.png)
    match = find_template_multiscale(screenshot, template)
    if match:
        x, y, w, h = match
        log(f"Connect button found at coordinates: x={x}, y={y}, width={w}, height={h}", level='INFO', device_id=device_id)
        # Perform tap action
        tap_x = x + w / 2  # Tap at the center of the detected image
        tap_y = y + h / 2

        # Adjust tap coordinates based on screen scaling
        tap_x_adj, tap_y_adj = adjust_tap_coordinates(tap_x, tap_y, (screenshot_width, screenshot_height), (screen_width, screen_height))

        tap_on_device(tap_x_adj, tap_y_adj)
        # Wait for the "Connect" button to disappear (optional)
        image_disappeared = wait_for_image_to_disappear(template, timeout=10, check_interval=2)
        if image_disappeared:
            log("Tap action confirmed. Connect button is no longer on the screen.", level='INFO', device_id=device_id)
        else:
            log("Connect button is still on the screen after tap action.", level='WARNING', device_id=device_id)

        # Wait for 30 seconds to confirm the "Stop" button appears
        connected = wait_for_image_to_appear(stop_template, timeout=30, check_interval=5)
        if connected:
            log("Device successfully connected.", level='INFO', device_id=device_id)
            # Press the home button to minimize the app
            press_home_button()
        else:
            log("Failed to confirm connection on device.", level='ERROR', device_id=device_id)
        cleanup()
    else:
        log("Connect button not found on the screen.", level='ERROR', device_id=device_id)
        cleanup()
        return

# Main function to process all devices
def main():
    set_working_directory()
    while True:
        devices = get_connected_devices()
        if not devices:
            log("No connected devices found. Exiting.", level='WARNING')
            return

        # Choose whether to process devices one by one or concurrently
        process_concurrently = True  # Set to False to process devices one by one

        log("Starting routine...", level='INFO')
        threads = []
        for device_id in devices:
            if process_concurrently:
                t = threading.Thread(target=process_device, args=(device_id,))
                threads.append(t)
                t.start()
            else:
                process_device(device_id)
        if process_concurrently:
            for t in threads:
                t.join()
        log("Routine completed. Waiting for 10 minutes before next run...", level='INFO')
        time.sleep(600)  # Wait for 600 seconds (10 minutes)

if __name__ == '__main__':
    main()
