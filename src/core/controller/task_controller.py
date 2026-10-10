from core.tools.registry import ToolRegistry
from core.tools.base import ToolResult
from core.controller.task import Task, TaskStatus


class TaskController:
    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    def execute_tool(self, tool_name: str, arguments: dict[str, object]) -> ToolResult:
        return self.registry.execute(tool_name, arguments)

    def execute_sequence(self, actions: list[dict[str, object]]) -> list[ToolResult]:
        results: list[ToolResult] = []

        for action in actions:
            tool_name = action["tool"]
            arguments = action["arguments"]

            if not isinstance(tool_name, str):
                raise TypeError("Tool name must be a string.")

            if not isinstance(arguments, dict):
                raise TypeError("Tool arguments must be a dictionary.")

            result = self.execute_tool(tool_name, arguments)
            results.append(result)

            if not result.success:
                break

        return results

    def execute_task(self, task: Task) -> Task:
        task.status = TaskStatus.RUNNING

        for step in task.steps:
            result = self.execute_tool(
                step.tool_name,
                step.arguments,
            )

            step.result = result

            if not result.success:
                task.status = TaskStatus.FAILED
                return task

        task.status = TaskStatus.SUCCESS
        return task
