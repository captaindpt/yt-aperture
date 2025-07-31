"""Configuration settings for YouTube Semantic Search."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchConfig:
    """Configuration for semantic search."""
    model_name: str = "all-MiniLM-L6-v2"
    cache_dir: str = "cache"
    batch_size: int = 32
    max_sentences_per_chunk: int = 6
    default_results: int = 10
    default_context_chunks: int = 3


@dataclass
class ExtractionConfig:
    """Configuration for YouTube extraction."""
    default_language: str = "en"
    output_dir: str = "."
    include_auto_subs: bool = True
    

@dataclass
class AppConfig:
    """Main application configuration."""
    search: SearchConfig
    extraction: ExtractionConfig
    
    @classmethod
    def from_env(cls) -> 'AppConfig':
        """Create configuration from environment variables."""
        search_config = SearchConfig(
            model_name=os.getenv("YSS_MODEL_NAME", "all-MiniLM-L6-v2"),
            cache_dir=os.getenv("YSS_CACHE_DIR", "cache"),
            batch_size=int(os.getenv("YSS_BATCH_SIZE", "32")),
            max_sentences_per_chunk=int(os.getenv("YSS_MAX_SENTENCES", "6")),
            default_results=int(os.getenv("YSS_DEFAULT_RESULTS", "10")),
            default_context_chunks=int(os.getenv("YSS_DEFAULT_CONTEXT", "3"))
        )
        
        extraction_config = ExtractionConfig(
            default_language=os.getenv("YSS_LANGUAGE", "en"),
            output_dir=os.getenv("YSS_OUTPUT_DIR", "."),
            include_auto_subs=bool(os.getenv("YSS_AUTO_SUBS", "true").lower() in ("true", "1", "yes"))
        )
        
        return cls(search=search_config, extraction=extraction_config)


# Default configuration instance
default_config = AppConfig.from_env()