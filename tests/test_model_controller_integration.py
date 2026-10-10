
import unittest
import needle

from core.controller.model_controller import ModelController
from core.controller.task_controller import TaskController
from core.permissions import PermissionGate
from core.tools import CalculatorTool, ToolRegistry


class TestModelControllerIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        gate = PermissionGate()
        registry = ToolRegistry(gate)
        registry.register(CalculatorTool())

        cls.agent = needle.Needle(tools=registry.get_model_tools())

        cls.task_controller = TaskController(registry)
        cls.controller = ModelController(cls.agent, cls.task_controller)

    def test_real_model_executes_calculation(self) -> None:
        results = self.controller.handle_request("Add 10 and 5.")

        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].success)
        self.assertEqual(results[0].data["result"], 15)

    
    def test_real_model_selects_multiple_tool_calls(self) -> None:
        results = self.controller.handle_request(
            "Calculate 10 plus 5, and separately calculate 20 plus 30."
        )

        self.assertEqual(len(results), 2)

        self.assertTrue(results[0].success)
        self.assertEqual(results[0].data["result"], 15)

        self.assertTrue(results[1].success)
        self.assertEqual(results[1].data["result"], 50)



if __name__ == "__main__":
    unittest.main()
