# model_factory.py

import os
from typing import Literal
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

Provider = Literal[
    "openai",
    "anthropic",
    "google",
    "deepseek",
    "qwen",
    "ollama",
]
load_dotenv()

class Model:
    @staticmethod
    def create_model(
        provider: Provider,
        model: str,
        temperature: float = 0,
        **kwargs,
    ):
        """
        Create a chat model instance for LangGraph / LangChain.
        """

        if provider == "openai":
            return ChatOpenAI(
                model=model,
                temperature=temperature,
                api_key=os.getenv("OPENAI_API_KEY"),
                **kwargs,
            )

        if provider == "anthropic":
            return ChatAnthropic(
                model=model,
                temperature=temperature,
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                **kwargs,
            )

        if provider == "google":
            return ChatGoogleGenerativeAI(
                model=model,
                temperature=temperature,
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                **kwargs,
            )

        if provider == "deepseek":
            return ChatOpenAI(
                model=model,
                temperature=temperature,
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url=os.getenv("DEEPSEEK_URL"),
                **kwargs,
            )

        if provider == "qwen":
            return ChatOpenAI(
                model=model,
                temperature=temperature,
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                base_url=os.getenv("DASHSCOPE_URL"),
                **kwargs,
            )

        if provider == "ollama":
            return ChatOllama(
                model=model,
                temperature=temperature,
                **kwargs,
            )

        raise ValueError(f"Unsupported model provider: {provider}")
