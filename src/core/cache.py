"""Embedding cache management."""

import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np


class EmbeddingCache:
    """Manages caching of embeddings for performance."""
    
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def get_cache_paths(self, transcript_name: str) -> tuple[Path, Path]:
        """Get cache file paths for a specific transcript."""
        transcript_cache_dir = self.cache_dir / transcript_name
        transcript_cache_dir.mkdir(parents=True, exist_ok=True)
        
        embeddings_path = transcript_cache_dir / "embeddings.pkl"
        chunks_path = transcript_cache_dir / "chunks.pkl"
        
        return embeddings_path, chunks_path
    
    def load_cache(self, transcript_name: str) -> Optional[tuple[np.ndarray, List[Dict[str, Any]]]]:
        """
        Load cached embeddings and chunks.
        
        Returns:
            Tuple of (embeddings, chunks) or None if cache invalid/missing
        """
        embeddings_path, chunks_path = self.get_cache_paths(transcript_name)
        
        if not (embeddings_path.exists() and chunks_path.exists()):
            return None
        
        try:
            with open(embeddings_path, 'rb') as f:
                embeddings = pickle.load(f)
            with open(chunks_path, 'rb') as f:
                chunks = pickle.load(f)
            
            return embeddings, chunks
            
        except Exception as e:
            print(f"⚠️  Error loading cache: {e}")
            return None
    
    def save_cache(
        self, 
        transcript_name: str, 
        embeddings: np.ndarray, 
        chunks: List[Dict[str, Any]]
    ) -> None:
        """Save embeddings and chunks to cache."""
        embeddings_path, chunks_path = self.get_cache_paths(transcript_name)
        
        try:
            with open(embeddings_path, 'wb') as f:
                pickle.dump(embeddings, f)
            with open(chunks_path, 'wb') as f:
                pickle.dump(chunks, f)
            
            print(f"✅ Cached {len(embeddings)} embeddings for {transcript_name}")
            
        except Exception as e:
            print(f"⚠️  Error saving cache: {e}")
    
    def is_cache_valid(self, transcript_name: str, chunks: List[Dict[str, Any]]) -> bool:
        """Check if cached data is still valid for current chunks."""
        cached_data = self.load_cache(transcript_name)
        if not cached_data:
            return False
        
        _, cached_chunks = cached_data
        return len(cached_chunks) == len(chunks)
    
    def clear_cache(self, transcript_name: Optional[str] = None) -> None:
        """Clear cache for specific transcript or all caches."""
        if transcript_name:
            transcript_cache_dir = self.cache_dir / transcript_name
            if transcript_cache_dir.exists():
                for file in transcript_cache_dir.iterdir():
                    file.unlink()
                transcript_cache_dir.rmdir()
                print(f"✅ Cleared cache for {transcript_name}")
        else:
            for item in self.cache_dir.iterdir():
                if item.is_dir():
                    for file in item.iterdir():
                        file.unlink()
                    item.rmdir()
                elif item.is_file():
                    item.unlink()
            print("✅ Cleared all caches")