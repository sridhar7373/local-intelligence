
from needle import Needle

from core.llm.base import BaseLLM


class NeedleLLM(BaseLLM):
    def __init__(self, tools: list[dict[str, object]] | None = None, system: str | None = None, weights: str | None = None) -> None:
        self.model = Needle(
            tools=tools,
            system=system,
            weights=weights,
            stateless=True,
        )

    def generate(self, prompt: str, tools: list[dict[str, object]] | None = None) -> dict[str, object]:
        response = self.model.complete(prompt)

        if not isinstance(response, dict):
            return {
                "success": False,
                "error": "INVALID_MODEL_RESPONSE",
            }

        return response

    def close(self) -> None:
        self.model.close()
