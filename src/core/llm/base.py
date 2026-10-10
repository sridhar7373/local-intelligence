
from abc import ABC, abstractmethod


class BaseLLM(ABC):
    @abstractmethod
    def generate(self, prompt: str, tools: list[dict[str, object]] | None = None) -> dict[str, object]:
        """Generate a response using the model and optional tools."""
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        """Release model resources."""
        raise NotImplementedError
