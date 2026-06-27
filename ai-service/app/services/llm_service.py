from app.core.config import ModelConfig
from app.core.model_factory import Model


class LLMService:
    def __init__(self, config: ModelConfig):
        self.config = config
        self.llm = Model.create_model(
            provider=config.provider,
            model=config.model,
            **self._build_model_kwargs(config),
        )

    async def chat(self, message: str) -> str:
        response = await self.llm.ainvoke(message)
        return response.content

    def chat_sync(self, message: str) -> str:
        response = self.llm.invoke(message)
        return response.content

    @staticmethod
    def _build_model_kwargs(config: ModelConfig) -> dict:
        kwargs = {
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
        }
        return {key: value for key, value in kwargs.items() if value is not None}
