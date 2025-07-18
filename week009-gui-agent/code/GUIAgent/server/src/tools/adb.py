import time
import subprocess
from ..util.base import ToolError

def get_file(src_path, dst_path):
    command = f"adb pull {src_path} {dst_path}"
    result = subprocess.run(command, capture_output=True, text=True, shell=False)
    if result.returncode == 0:
        print("Get file succedded.")
    else:
        raise ToolError(f"Get file failed: {str(command)}")

def get_screenshot(screenshot_path):
    adb_screenshot_file = "/sdcard/screenshot.png"
    command = f"adb shell screenshot -p {adb_screenshot_file}"
    result = subprocess.run(command, capture_output=True, text=True, shell=False)
    if result.returncode == 0:
        print("Screen capture succedded.")
    else:
        raise ToolError(f"Screen capture failed: {str(command)}")
    
    get_file(adb_screenshot_file, screenshot_path)
