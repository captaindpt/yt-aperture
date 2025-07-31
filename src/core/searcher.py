"""Semantic search engine for transcripts."""

from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from .processor import TextProcessor
from .cache import EmbeddingCache


class SemanticSearcher:
    """Semantic search engine for transcript content."""
    
    def __init__(
        self, 
        model_name: str = "all-MiniLM-L6-v2",
        cache_dir: str = "cache"
    ):
        self.model = SentenceTransformer(model_name)
        self.cache = EmbeddingCache(cache_dir)
        self.processor = TextProcessor()
        
        self.transcript_name: Optional[str] = None
        self.chunks: List[Dict[str, Any]] = []
        self.embeddings: Optional[np.ndarray] = None
    
    def load_transcript(self, transcript_path: str) -> None:
        """Load and process transcript for searching."""
        transcript_path = Path(transcript_path)
        if not transcript_path.exists():
            raise FileNotFoundError(f"Transcript not found: {transcript_path}")
        
        self.transcript_name = transcript_path.stem
        
        print("Loading transcript...")
        with open(transcript_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Process transcript into chunks
        raw_chunks = self.processor.chunk_transcript(content)
        self.chunks = self.processor.split_large_chunks(raw_chunks)
        
        print(f"Created {len(self.chunks)} chunks from transcript")
        
        # Load or create embeddings
        self._load_or_create_embeddings()
    
    def _load_or_create_embeddings(self) -> None:
        """Load cached embeddings or create new ones."""
        if not self.transcript_name:
            raise ValueError("No transcript loaded")
        
        # Try to load from cache
        if self.cache.is_cache_valid(self.transcript_name, self.chunks):
            print("Loading cached embeddings...")
            cached_data = self.cache.load_cache(self.transcript_name)
            if cached_data:
                self.embeddings, _ = cached_data
                print("✅ Using cached embeddings")
                return
        
        print("Creating embeddings for all chunks...")
        texts = [chunk['content'] for chunk in self.chunks]
        
        # Create embeddings in batches
        batch_size = 32
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.model.encode(batch, show_progress_bar=True)
            embeddings.extend(batch_embeddings)
        
        self.embeddings = np.array(embeddings)
        
        # Cache the results
        self.cache.save_cache(self.transcript_name, self.embeddings, self.chunks)
    
    def search(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """
        Perform semantic search on the loaded transcript.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results with relevance scores
        """
        if self.embeddings is None or not self.chunks:
            raise ValueError("No transcript loaded. Call load_transcript() first.")
        
        print(f"🔍 Searching for: '{query}'")
        
        # Create query embedding
        query_embedding = self.model.encode([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top results
        top_indices = np.argsort(similarities)[::-1][:num_results]
        
        results = []
        for idx in top_indices:
            chunk_idx = int(idx)
            similarity_score = similarities[idx]
            
            chunk = self.chunks[chunk_idx]
            snippet = self.processor.extract_snippet(chunk['content'])
            
            result = {
                'id': chunk_idx,
                'similarity': similarity_score,
                'speaker': chunk['speaker'],
                'snippet': snippet,
                'full_content': chunk['content'],
                'original': chunk['original']
            }
            results.append(result)
        
        return results
    
    def get_expanded_context(
        self, 
        result_id: int, 
        context_chunks: int = 3
    ) -> str:
        """
        Get expanded context around a specific search result.
        
        Args:
            result_id: ID of the result to expand
            context_chunks: Number of chunks before/after to include
            
        Returns:
            Formatted text with expanded context
        """
        if result_id >= len(self.chunks):
            return f"Error: Result ID {result_id} not found"
        
        # Get context range
        start_idx = max(0, result_id - context_chunks)
        end_idx = min(len(self.chunks), result_id + context_chunks + 1)
        
        context_chunks_list = self.chunks[start_idx:end_idx]
        
        # Build context with main result highlighted
        context_text = ""
        for i, chunk in enumerate(context_chunks_list):
            if start_idx + i == result_id:
                context_text += f"\n>>> MAIN RESULT <<<\n"
                context_text += chunk['original'] + "\n"
                context_text += ">>> END RESULT <<<\n\n"
            else:
                context_text += chunk['original'] + "\n\n"
        
        return context_text.strip()
    
    def print_results(self, results: List[Dict[str, Any]]) -> None:
        """Print search results in a formatted way."""
        print(f"\n🎯 Found {len(results)} results:\n")
        
        for i, result in enumerate(results, 1):
            print(f"[{result['id']}] {result['speaker']} (Score: {result['similarity']:.3f})")
            print(f"    {result['snippet']}")
            print()
        
        if results:
            print("💡 Use --expand [ID] to see full context around a specific result")