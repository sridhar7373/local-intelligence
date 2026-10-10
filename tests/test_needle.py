import unittest

import needle


class TestNeedle(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        tools = [
            {
                "name": "math.add",
                "description": "Add two integers together.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "integer"},
                        "b": {"type": "integer"},
                    },
                    "required": ["a", "b"],
                },
            }
        ]

        cls.agent = needle.Needle(tools=tools)

    
    def test_selects_calculator_tool(self) -> None:
        result = self.agent.complete("Add 10 and 5.")

        self.assertTrue(result["success"])
        self.assertEqual(result["type"], "call")
        self.assertEqual(len(result["function_calls"]), 1)

        function_call = result["function_calls"][0]

        self.assertEqual(function_call["name"], "math.add")
        self.assertEqual(
            function_call["arguments"],
            {"a": 10, "b": 5},
        )



if __name__ == "__main__":
    unittest.main()
