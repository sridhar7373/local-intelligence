
import unittest

from core.tools import BaseTool


class TestBaseTool(unittest.TestCase):
    def test_tool_properties(self):
        tool = BaseTool("example.test", "A test tool", "data.read")

        self.assertEqual(tool.name, "example.test")
        self.assertEqual(tool.description, "A test tool")
        self.assertEqual(tool.capability, "data.read")


if __name__ == "__main__":
    unittest.main()
