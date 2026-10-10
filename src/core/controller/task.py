from dataclasses import dataclass, field
from enum import Enum

from core.tools.base import ToolResult


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class TaskStep:
    tool_name: str
    arguments: dict[str, object]
    result: ToolResult | None = None


@dataclass
class Task:
    name: str
    steps: list[TaskStep] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING