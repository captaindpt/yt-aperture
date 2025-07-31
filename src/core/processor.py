"""Text processing and formatting utilities."""

import re
from pathlib import Path
from typing import List, Dict, Any


class TextProcessor:
    """Handles text cleaning and formatting for transcripts."""
    
    @staticmethod
    def clean_transcript(input_file: Path, output_file: Path) -> None:
        """Remove consecutive duplicate lines from transcript."""
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Remove consecutive duplicates
        cleaned_lines = []
        prev_line = ""
        
        for line in lines:
            line = line.strip()
            if line and line != prev_line:
                cleaned_lines.append(line)
                prev_line = line
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(cleaned_lines))
    
    @staticmethod
    def chunk_transcript(content: str) -> List[Dict[str, Any]]:
        """
        Chunk transcript content for semantic search.
        
        Handles both speaker-formatted transcripts and generic text.
        """
        lines = content.split('\n')
        chunks = []
        current_chunk = []
        current_speaker = None
        
        # Try speaker-based chunking first
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and headers
            if not line or line.startswith('#') or line.startswith('**Transcript extracted'):
                continue
            
            # Check for speaker format
            if line.startswith('**DHH:**') or line.startswith('**Interviewer:**'):
                # Save previous chunk
                if current_chunk and current_speaker:
                    chunk_text = '\n'.join(current_chunk)
                    if len(chunk_text.strip()) > 20:
                        chunks.append({
                            'content': chunk_text,
                            'speaker': current_speaker,
                            'original': f"**{current_speaker}:** {chunk_text}"
                        })
                
                # Start new chunk
                current_speaker = "DHH" if line.startswith('**DHH:**') else "Interviewer"
                current_chunk = [line.replace(f'**{current_speaker}:**', '').strip()]
            else:
                if current_chunk is not None:
                    current_chunk.append(line)
        
        # Add final chunk
        if current_chunk and current_speaker:
            chunk_text = '\n'.join(current_chunk)
            if len(chunk_text.strip()) > 20:
                chunks.append({
                    'content': chunk_text,
                    'speaker': current_speaker,
                    'original': f"**{current_speaker}:** {chunk_text}"
                })
        
        # If no speaker format detected, use paragraph-based chunking
        if not chunks:
            paragraphs = content.split('\n\n')
            for para in paragraphs:
                para = para.strip()
                if (para and 
                    not para.startswith('#') and 
                    not para.startswith('**Transcript extracted') and
                    len(para) > 20):
                    chunks.append({
                        'content': para,
                        'speaker': 'Speaker',
                        'original': para
                    })
        
        return chunks
    
    @staticmethod
    def split_large_chunks(chunks: List[Dict[str, Any]], max_sentences: int = 6) -> List[Dict[str, Any]]:
        """Split large chunks into smaller ones for better search granularity."""
        final_chunks = []
        
        for chunk in chunks:
            sentences = re.split(r'[.!?]+', chunk['content'])
            sentences = [s.strip() for s in sentences if s.strip()]
            
            if len(sentences) <= max_sentences:
                # Keep small chunks as is
                final_chunks.append({
                    'id': len(final_chunks),
                    'content': chunk['content'],
                    'original': chunk['original'],
                    'speaker': chunk['speaker'],
                    'start_index': len(final_chunks)
                })
            else:
                # Split large chunks
                for i in range(0, len(sentences), max_sentences):
                    sentence_group = sentences[i:i + max_sentences]
                    sub_chunk_content = '. '.join(sentence_group)
                    if not sub_chunk_content.endswith('.'):
                        sub_chunk_content += '.'
                    
                    if len(sub_chunk_content.strip()) > 20:
                        final_chunks.append({
                            'id': len(final_chunks),
                            'content': sub_chunk_content,
                            'original': f"**{chunk['speaker']}:** {sub_chunk_content}",
                            'speaker': chunk['speaker'],
                            'start_index': len(final_chunks)
                        })
        
        return final_chunks
    
    @staticmethod
    def extract_snippet(text: str, max_sentences: int = 2) -> str:
        """Extract a brief snippet from text."""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= max_sentences:
            return text
        
        snippet = '. '.join(sentences[:max_sentences])
        if not snippet.endswith('.'):
            snippet += '.'
        
        return snippet