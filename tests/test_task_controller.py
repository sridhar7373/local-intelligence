import unittest

from core.controller import Task, TaskStep, TaskStatus, TaskController
from core.permissions import PermissionGate
from core.tools import CalculatorTool, ToolRegistry


class TestTaskController(unittest.TestCase):
    def setUp(self) -> None:
        gate = PermissionGate()
        registry = ToolRegistry(gate)
        registry.register(CalculatorTool())

        self.controller = TaskController(registry)

    def test_execute_tool(self) -> None:
        result = self.controller.execute_tool(
            "math.add",
            {"a": 10, "b": 5},
        )

        self.assertTrue(result.success)
        self.assertEqual(result.data["result"], 15)

    def test_execute_sequence(self) -> None:
        actions = [
            {
                "tool": "math.add",
                "arguments": {"a": 10, "b": 5},
            },
            {
                "tool": "math.add",
                "arguments": {"a": 20, "b": 30},
            },
        ]

        results = self.controller.execute_sequence(actions)

        self.assertEqual(len(results), 2)
        self.assertTrue(results[0].success)
        self.assertTrue(results[1].success)
        self.assertEqual(results[0].data["result"], 15)
        self.assertEqual(results[1].data["result"], 50)

    def test_task_stops_when_a_step_fails(self) -> None:
        task = Task(
            name="Test failure handling",
            steps=[
                TaskStep("math.add", {"a": 10, "b": 5}),
                TaskStep("math.add", {"a": "invalid", "b": 5}),
                TaskStep("math.add", {"a": 20, "b": 30}),
            ],
        )

        result = self.controller.execute_task(task)

        self.assertEqual(result.status, TaskStatus.FAILED)
        self.assertIsNotNone(result.steps[0].result)
        self.assertTrue(result.steps[0].result.success)

        self.assertIsNotNone(result.steps[1].result)
        self.assertFalse(result.steps[1].result.success)

        self.assertIsNone(result.steps[2].result)


if __name__ == "__main__":
    unittest.main()
