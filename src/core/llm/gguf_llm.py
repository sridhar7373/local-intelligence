
from pathlib import Path

from llama_cpp import Llama

from core.llm.base import BaseLLM


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "LFM2.5-350M-Q4_K_M.gguf"



class GGUFLLM(BaseLLM):
    def __init__(self, tools: list[dict[str, object]] | None = None, model_path: str | Path = DEFAULT_MODEL_PATH, context_size: int = 4096, max_tokens: int = 512) -> None:
        self.model_path = Path(model_path).resolve()
        self.max_tokens = max_tokens
        self.tools = tools or []

        if not self.model_path.is_file():
            raise FileNotFoundError(f"GGUF model file not found: {self.model_path}")

        self.model = Llama(
            model_path=str(self.model_path),
            n_ctx=context_size,
            verbose=False,
        )


    def generate(self, prompt: str) -> dict[str, object]:
        try:
            response = self.model.create_chat_completion(
                messages=[
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.max_tokens,
                temperature=0.0,
            )

            choices = response.get("choices", [])
            if not choices:
                return {
                    "success": False,
                    "error": "EMPTY_MODEL_RESPONSE",
                }

            message = choices[0].get("message", {})
            content = message.get("content")

            return {
                "success": True,
                "text": content if isinstance(content, str) else "",
                "function_calls": [],
            }

        except Exception:
            return {
                "success": False,
                "error": "MODEL_GENERATION_FAILED",
            }

    def close(self) -> None:
        close = getattr(self.model, "close", None)
        if callable(close):
            close()
