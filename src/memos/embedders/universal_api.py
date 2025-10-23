from openai import AzureOpenAI as AzureClient
from openai import OpenAI as OpenAIClient

from memos.configs.embedder import UniversalAPIEmbedderConfig
from memos.embedders.base import BaseEmbedder
from memos.log import get_logger

logger = get_logger(__name__)


class UniversalAPIEmbedder(BaseEmbedder):
    def __init__(self, config: UniversalAPIEmbedderConfig):
        self.provider = config.provider
        self.config = config

        if self.provider == "openai":
            self.client = OpenAIClient(api_key=config.api_key, base_url=config.base_url)
        elif self.provider == "azure":
            self.client = AzureClient(
                azure_endpoint=config.base_url,
                api_version="2024-03-01-preview",
                api_key=config.api_key,
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def embed(self, texts: list[str]) -> list[list[float]]:
        # Check for potential truncation issues
        # Note: This is a safety check for BGE-Large (512 token limit) or similar models
        MAX_EMBEDDING_TOKENS = 512  # Common limit for many models (BGE-Large, etc.)
        for i, text in enumerate(texts):
            # Rough estimate: 1 token ≈ 4 characters
            estimated_tokens = len(text) // 4
            if estimated_tokens > MAX_EMBEDDING_TOKENS:
                logger.warning(
                    f"⚠️  TRUNCATION RISK: Text {i} has ~{estimated_tokens} tokens (estimated), "
                    f"exceeds embedding model limit of {MAX_EMBEDDING_TOKENS}. "
                    f"Consider using smaller chunk_size or check if auto-truncate is enabled."
                )

        if self.provider == "openai" or self.provider == "azure":
            response = self.client.embeddings.create(
                model=getattr(self.config, "model_name_or_path", "text-embedding-3-large"),
                input=texts,
            )
            return [r.embedding for r in response.data]
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
