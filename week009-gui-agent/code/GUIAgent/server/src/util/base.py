from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field, replace
from typing import Any

class ToolError(Exception):
    """
    Raised when a tool encounters an error
    """
    def __init__(self, message):
        self.message = message
