from core.llm import NeedleLLM
from core.controller.model_controller import ModelController
from core.controller.task_controller import TaskController
from core.permissions import PermissionGate
from core.tools import AddTool, SubtractTool, MultiplyTool, DivideTool, ToolRegistry



def main() -> None:
    gate = PermissionGate()
    registry = ToolRegistry(gate)
    registry.register(AddTool())
    registry.register(SubtractTool())
    registry.register(MultiplyTool())
    registry.register(DivideTool())

    llm = NeedleLLM(tools=registry.get_model_tools())

    try:
        task_controller = TaskController(registry)
        model_controller = ModelController(
            llm=llm,
            task_controller=task_controller,
        )

        print("Local Intelligence")
        print("Type 'exit' to quit.")

        while True:
            try:
                request = input("\nYou: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break

            if request.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            if not request:
                continue

            results = model_controller.handle_request(request)

            for result in results:
                if result.success:
                    print("Result:", result.data or result.message)
                else:
                    print("Error:", result.error or result.message)
    finally:
        llm.close()


if __name__ == "__main__":
    main()

