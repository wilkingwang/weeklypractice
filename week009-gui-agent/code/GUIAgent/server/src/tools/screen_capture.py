import os
import cv2
from pathlib import Path
from uuid import uuid4
from io import BytesIO
from PIL import Image
from .base import ToolError
from adb import get_screenshot

OUTPUT_DIR = "./tmp/outputs"

def get_screenshot(resize: bool = False, target_width: int = 1920, target_height: int = 1080):
    """
    Capture screenshot by requsting from adb
    returns native resulution unless resized
    """
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = output_dir / f"screenshot_{uuid4().hex}.png"

    try:
        get_screenshot(screenshot_path)

        if not os.path.exists(screenshot_path):
            raise ToolError(f"Screenshot file not exist.")
        
        screenshot = cv2.imread(screenshot_path)
        if screenshot is None:
            raise ToolError(f"Screenshot cannot be opened.")
        
        screenshot_img = Image.open(BytesIO(screenshot))

        if resize and screenshot_img.size != (target_width, target_height):
            screenshot_img = screenshot_img.resize((target_width, target_height))

        screenshot_img.save(screenshot_path)

        return screenshot_path
    except Exception as e:
        raise ToolError(f"Failed to capture screenshot: {str(e)}")
