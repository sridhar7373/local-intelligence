
from core.tools.base import BaseTool, ToolResult


class ArithmeticTool(BaseTool):
    def __init__(self, name: str, description: str, operation: str) -> None:
        super().__init__(
            name=name,
            description=description,
            capability="data.calculate",
        )

        self.operation = operation

        self.parameters: dict[str, type] = {
            "a": float,
            "b": float,
        }

        self.parameter_schema = {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "The first number.",
                },
                "b": {
                    "type": "number",
                    "description": "The second number.",
                },
            },
            "required": ["a", "b"],
        }

    def execute(self, arguments: dict[str, object]) -> ToolResult:
        a = arguments["a"]
        b = arguments["b"]

        if self.operation == "add":
            result = a + b
        elif self.operation == "subtract":
            result = a - b
        elif self.operation == "multiply":
            result = a * b
        elif self.operation == "divide":
            if b == 0:
                return ToolResult(
                    success=False,
                    message="Cannot divide by zero.",
                    error="DIVISION_BY_ZERO",
                )

            result = a / b
        else:
            return ToolResult(
                success=False,
                message="Unsupported arithmetic operation.",
                error="INVALID_OPERATION",
            )

        return ToolResult(
            success=True,
            data={"result": result},
            message="Calculation completed.",
        )


class AddTool(ArithmeticTool):
    def __init__(self) -> None:
        super().__init__(
            name="math.add",
            description="Add two numbers together.",
            operation="add",
        )


class SubtractTool(ArithmeticTool):
    def __init__(self) -> None:
        super().__init__(
            name="math.subtract",
            description="Subtract the second number from the first.",
            operation="subtract",
        )


class MultiplyTool(ArithmeticTool):
    def __init__(self) -> None:
        super().__init__(
            name="math.multiply",
            description="Multiply two numbers together.",
            operation="multiply",
        )


class DivideTool(ArithmeticTool):
    def __init__(self) -> None:
        super().__init__(
            name="math.divide",
            description="Divide the first number by the second.",
            operation="divide",
        )
