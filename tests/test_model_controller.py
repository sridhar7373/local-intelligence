import unittest

from core.controller import ModelController
from core.controller import TaskController
from core.permissions import PermissionGate
from core.tools import CalculatorTool, ToolRegistry


class FakeNeedleAgent:
    def __init__(self, response: dict[str, object]) -> None:
        self.response = response

    def complete(self, request: str) -> dict[str, object]:
        return self.response


class TestModelController(unittest.TestCase):
    def setUp(self) -> None:
        gate = PermissionGate()
        registry = ToolRegistry(gate)
        registry.register(CalculatorTool())

        self.task_controller = TaskController(registry)

    def test_multiple_tool_calls(self) -> None:
        agent = FakeNeedleAgent({
            "success": True,
            "function_calls": [
                {
                    "name": "math.add",
                    "arguments": {"a": 10, "b": 5},
                },
                {
                    "name": "math.add",
                    "arguments": {"a": 20, "b": 30},
                },
            ],
        })

        controller = ModelController(agent, self.task_controller)
        results = controller.handle_request("Add 10 and 5, then add 20 and 30.")

        self.assertEqual(len(results), 2)
        self.assertTrue(results[0].success)
        self.assertTrue(results[1].success)
        self.assertEqual(results[0].data["result"], 15)
        self.assertEqual(results[1].data["result"], 50)

    def test_stops_when_a_tool_fails(self) -> None:
        agent = FakeNeedleAgent({
            "success": True,
            "function_calls": [
                {
                    "name": "math.add",
                    "arguments": {"a": 10, "b": 5},
                },
                {
                    "name": "math.add",
                    "arguments": {"a": "invalid", "b": 5},
                },
                {
                    "name": "math.add",
                    "arguments": {"a": 20, "b": 30},
                },
            ],
        })

        controller = ModelController(agent, self.task_controller)
        results = controller.handle_request("Perform three calculations.")

        self.assertEqual(len(results), 2)
        self.assertTrue(results[0].success)
        self.assertFalse(results[1].success)

    def test_model_failure(self) -> None:
        agent = FakeNeedleAgent({
            "success": False,
            "error": "Model inference failed.",
            "function_calls": [],
        })

        controller = ModelController(agent, self.task_controller)
        results = controller.handle_request("Add 10 and 5.")

        self.assertEqual(len(results), 1)
        self.assertFalse(results[0].success)
        self.assertEqual(results[0].error, "Model inference failed.")


if __name__ == "__main__":
    unittest.main()
