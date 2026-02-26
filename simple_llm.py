from langchain_core.language_models.llms import LLM
from typing import Optional, List


class SimpleLLM(LLM):

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        return f"According to our policy:\n\n{prompt}"

    @property
    def _identifying_params(self):
        return {}

    @property
    def _llm_type(self):
        return "simple-llm"