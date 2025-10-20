from memos.configs.chunker import SentenceChunkerConfig
from memos.dependency import require_python_package
from memos.log import get_logger

from .base import BaseChunker, Chunk


logger = get_logger(__name__)


class SentenceChunker(BaseChunker):
    """Sentence-based text chunker."""

    @require_python_package(
        import_name="chonkie",
        install_command="pip install chonkie",
        install_link="https://docs.chonkie.ai/python-sdk/getting-started/installation",
    )
    def __init__(self, config: SentenceChunkerConfig):
        from chonkie import SentenceChunker as ChonkieSentenceChunker

        self.config = config

        # If tokenizer_or_token_counter is a string (model name), try to load it from cache first
        tokenizer = config.tokenizer_or_token_counter
        if isinstance(tokenizer, str):
            try:
                import os
                from transformers import AutoTokenizer

                # Temporarily unset HF_ENDPOINT to prevent connection attempts
                original_hf_endpoint = os.environ.get('HF_ENDPOINT')
                if original_hf_endpoint:
                    os.environ.pop('HF_ENDPOINT', None)

                try:
                    logger.info(f"Loading tokenizer '{tokenizer}' from local cache...")
                    tokenizer = AutoTokenizer.from_pretrained(tokenizer, local_files_only=True)
                    logger.info(f"Successfully loaded tokenizer from cache: {type(tokenizer).__name__}")
                finally:
                    # Restore HF_ENDPOINT
                    if original_hf_endpoint:
                        os.environ['HF_ENDPOINT'] = original_hf_endpoint
            except Exception as e:
                logger.warning(f"Failed to load tokenizer from cache: {e}. Will pass string to Chonkie.")
                tokenizer = config.tokenizer_or_token_counter

        self.chunker = ChonkieSentenceChunker(
            tokenizer_or_token_counter=tokenizer,
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            min_sentences_per_chunk=config.min_sentences_per_chunk,
        )
        logger.info(f"Initialized SentenceChunker with config: {config}")

    def chunk(self, text: str) -> list[Chunk]:
        """Chunk the given text into smaller chunks based on sentences."""
        chonkie_chunks = self.chunker.chunk(text)

        chunks = []
        for c in chonkie_chunks:
            chunk = Chunk(text=c.text, token_count=c.token_count, sentences=c.sentences)
            chunks.append(chunk)

        logger.debug(f"Generated {len(chunks)} chunks from input text")
        return chunks
