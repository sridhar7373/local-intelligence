from core.permissions.gate import PermissionGate
from core.tools.base import BaseTool, ToolResult
from core.tools.validator import validate_arguments


class ToolRegistry:
    def __init__(self, permission_gate: PermissionGate) -> None:
        self.tools: dict[str, BaseTool] = {}
        self.permission_gate = permission_gate

    def register(self, tool: BaseTool) -> None:
        if tool.name in self.tools:
            raise ValueError(f"Tool already registered: {tool.name}")

        self.tools[tool.name] = tool

    def get(self, name: str) -> BaseTool:
        if name not in self.tools:
            raise KeyError(f"Tool not found: {name}")

        return self.tools[name]

    def get_model_tools(self) -> list[dict[str, object]]:
        return [tool.to_model_tool() for tool in self.tools.values()]

    def list_tools(self) -> list[BaseTool]:
        return list(self.tools.values())

    def execute(self, name: str, arguments: dict[str, object]) -> ToolResult:
        try:
            tool = self.get(name)

            validate_arguments(arguments, tool.parameters)

            decision = self.permission_gate.check(tool.capability)

            if not decision.allowed:
                return ToolResult(
                    success=False,
                    message="Permission denied.",
                    error=decision.reason,
                )

            return tool.execute(arguments)

        except (ValueError, TypeError, KeyError) as error:
            return ToolResult(
                success=False,
                message="Tool request failed.",
                error=str(error),
            )
        except Exception:
            return ToolResult(
                success=False,
                message="Tool execution failed unexpectedly.",
                error="UNEXPECTED_ERROR",
            )