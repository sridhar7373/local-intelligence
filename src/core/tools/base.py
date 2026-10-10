
from dataclasses import dataclass, field


@dataclass
class ToolResult:
    success: bool
    data: dict[str, object] = field(default_factory=dict)
    message: str = ""
    error: str | None = None



class BaseTool:
    def __init__(self, name: str, description: str, capability: str) -> None:
        self.name = name
        self.description = description
        self.capability = capability

        # Runtime types used by the validator.
        self.parameters: dict[str, type] = {}

        # Model-independent JSON Schema for tool arguments.
        self.parameter_schema: dict[str, object] = {
            "type": "object",
            "properties": {},
            "required": [],
        }

    def to_model_tool(self) -> dict[str, object]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameter_schema,
        }

    def execute(self, arguments: dict[str, object]) -> ToolResult:
        raise NotImplementedError(
            "Every tool must implement execute()."
        )
