
from core.llm.base import BaseLLM
from core.controller.task_controller import TaskController
from core.tools.base import ToolResult


class ModelController:
    def __init__(self, llm: BaseLLM, task_controller: TaskController) -> None:
        self.llm = llm
        self.task_controller = task_controller

    def handle_request(self, request: str) -> list[ToolResult]:
        response = self.llm.generate(request)
        print("LLM response:", repr(response))

        if not response.get("success"):
            return [
                ToolResult(
                    success=False,
                    message="The model could not process the request.",
                    error=response.get("error") or "MODEL_ERROR",
                )
            ]

        function_calls = response.get("function_calls", [])

        if not isinstance(function_calls, list):
            return [
                ToolResult(
                    success=False,
                    message="Invalid model response.",
                    error="INVALID_TOOL_CALLS",
                )
            ]

        if not function_calls:
            text = response.get("text", "")
            return [
                ToolResult(
                    success=True,
                    message=text if isinstance(text, str) and text else "No response generated.",
                )
            ]

        actions: list[dict[str, object]] = []

        for function_call in function_calls:
            if not isinstance(function_call, dict):
                return [
                    ToolResult(
                        success=False,
                        message="Invalid tool call.",
                        error="INVALID_TOOL_CALL",
                    )
                ]

            tool_name = function_call.get("name")
            arguments = function_call.get("arguments")

            if not isinstance(tool_name, str):
                return [
                    ToolResult(
                        success=False,
                        message="Invalid tool name.",
                        error="INVALID_TOOL_NAME",
                    )
                ]

            if not isinstance(arguments, dict):
                return [
                    ToolResult(
                        success=False,
                        message="Invalid tool arguments.",
                        error="INVALID_ARGUMENTS",
                    )
                ]

            actions.append({
                "tool": tool_name,
                "arguments": arguments,
            })

        return self.task_controller.execute_sequence(actions)
