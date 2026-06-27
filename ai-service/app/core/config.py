from dataclasses import dataclass


@dataclass
class ModelConfig:
    provider: str
    model: str
    temperature: float = 1.0
    max_tokens: int | None = None