import json
from abc import ABC, abstractmethod
from typing import Any

from ollama import AsyncClient, ResponseError

from app.config import settings
from app.log_config.logger import get_logger
from app.utils.retry import async_retry


class BaseAgent(ABC):
    def __init__(self):
        headers = {}
        if settings.ollama_api_key:
            headers["Authorization"] = f"Bearer {settings.ollama_api_key}"
        self.client = AsyncClient(
            host=settings.ollama_base_url,
            headers=headers,
        )
        self.logger = get_logger(self.__class__.__name__)
        self.model = settings.ollama_model

    @abstractmethod
    def system_prompt(self) -> str:
        ...

    @abstractmethod
    def parse_response(self, response: str) -> Any:
        ...

    @async_retry(max_retries=settings.max_retries, delay=settings.retry_delay)
    async def call_llm(self, messages: list[dict], temperature: float = 0.3) -> str:
        self.logger.info(
            "Calling LLM",
            extra={"model": self.model, "messages_count": len(messages)},
        )
        response = await self.client.chat(
            model=self.model,
            messages=messages,
        )
        content = response["message"]["content"]
        self.logger.info("LLM response received")
        return content

    async def run(self, **kwargs) -> Any:
        system = self.system_prompt()
        user_content = self.build_user_prompt(**kwargs)

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_content},
        ]

        try:
            raw_response = await self.call_llm(messages)
            return self.parse_response(raw_response)
        except (ResponseError, Exception) as e:
            self.logger.warning(
                "LLM call failed, caller should handle fallback",
                extra={"error": str(e), "agent": self.__class__.__name__},
            )
            raise

    def build_user_prompt(self, **kwargs) -> str:
        parts = []
        for key, value in kwargs.items():
            if value is not None:
                if isinstance(value, (list, dict)):
                    parts.append(f"{key}:\n{json.dumps(value, indent=2)}")
                else:
                    parts.append(f"{key}: {value}")
        return "\n\n".join(parts)
