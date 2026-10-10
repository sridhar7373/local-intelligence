
import unittest

from core.permissions import PermissionGate
from core.tools import CalculatorTool, ToolRegistry


class TestToolRegistry(unittest.TestCase):
    def setUp(self) -> None:
        self.gate = PermissionGate()
        self.registry = ToolRegistry(self.gate)
        self.calculator = CalculatorTool()

        self.registry.register(self.calculator)

    def test_register_tool(self) -> None:
        tool = self.registry.get("math.add")

        self.assertIs(tool, self.calculator)

    def test_list_tools(self) -> None:
        tools = self.registry.list_tools()

        self.assertEqual(len(tools), 1)
        self.assertEqual(tools[0].name, "math.add")

    def test_duplicate_registration(self) -> None:
        with self.assertRaises(ValueError):
            self.registry.register(CalculatorTool())

    def test_execute_tool(self) -> None:
        result = self.registry.execute("math.add", {"a": 10, "b": 5})

        self.assertTrue(result.success)
        self.assertEqual(result.data["result"], 15)

    def test_invalid_arguments(self) -> None:
        result = self.registry.execute("math.add", {"a": "ten", "b": 5})

        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)

    def test_missing_tool(self) -> None:
        result = self.registry.execute("math.subtract", {"a": 10, "b": 5})

        self.assertFalse(result.success)
        self.assertIn("Tool not found", result.error)

    def test_permission_denied(self) -> None:
        restricted_gate = PermissionGate()
        restricted_gate.allowed_capabilities.clear()

        restricted_registry = ToolRegistry(restricted_gate)
        restricted_registry.register(CalculatorTool())

        result = restricted_registry.execute("math.add", {"a": 10, "b": 5})

        self.assertFalse(result.success)
        self.assertEqual(result.message, "Permission denied.")


if __name__ == "__main__":
    unittest.main()
