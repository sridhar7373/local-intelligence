
import unittest

from core.tools import CalculatorTool


class TestCalculatorTool(unittest.TestCase):
    def test_add_two_numbers(self) -> None:
        tool = CalculatorTool()

        result = tool.execute({
            "a": 10,
            "b": 5,
        })

        self.assertTrue(result.success)
        self.assertEqual(result.data["result"], 15)
        self.assertEqual(result.message, "Calculation completed.")
        self.assertIsNone(result.error)


if __name__ == "__main__":
    unittest.main()
