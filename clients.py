import os
from openai import AsyncOpenAI

class ModelClient:
    def __init__(self, client: AsyncOpenAI):
        self.client = client

    @classmethod
    def from_provider(cls, provider: str) -> 'ModelClient':
        """
        Create a ModelClient instance from a provider key.

        Args:
            provider: One of 'openai', 'groq', or 'gemini'

        Returns:
            ModelClient: Configured client for the specified provider

        Raises:
            ValueError: If provider is not supported
        """

        provider_configs = {
            'openai': {
                'base_url': '',
                'api_key_env': 'OPENAI_API_KEY'
            },
            'groq': {
                'base_url': 'https://api.groq.com/openai/v1',
                'api_key_env': 'GROQ_API_KEY'
            },
            'gemini': {
                'base_url': 'https://generativelanguage.googleapis.com/v1beta/openai/',
                'api_key_env': 'GEMINI_API_KEY'
            }
        }

        if provider not in provider_configs:
            raise ValueError(f"Unsupported provider: {provider}. Must be one of: {list(provider_configs.keys())}")

        config = provider_configs[provider]
        api_key = os.getenv(config['api_key_env'])

        if not api_key:
            raise ValueError(f"Environment variable {config['api_key_env']} not found")

        if provider == 'openai':
            client = AsyncOpenAI()
        else:
            client = AsyncOpenAI(
                api_key=api_key,
                base_url=config['base_url']
            )

        return cls(client)
