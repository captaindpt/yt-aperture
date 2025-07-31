"""Tests for text processing functionality."""

import pytest
from src.core.processor import TextProcessor


class TestTextProcessor:
    """Test cases for TextProcessor class."""
    
    def test_extract_snippet(self):
        """Test snippet extraction functionality."""
        processor = TextProcessor()
        
        # Test short text (should return as-is)
        short_text = "This is a short sentence."
        result = processor.extract_snippet(short_text, max_sentences=2)
        assert result == short_text
        
        # Test long text (should truncate)
        long_text = "First sentence. Second sentence. Third sentence. Fourth sentence."
        result = processor.extract_snippet(long_text, max_sentences=2)
        assert result == "First sentence. Second sentence."
    
    def test_chunk_transcript_generic(self):
        """Test chunking of generic transcript without speaker labels."""
        processor = TextProcessor()
        
        content = """**Transcript extracted from YouTube video**

This is the first paragraph.
It has multiple lines.

This is the second paragraph.
Also with multiple lines.

This is a very short paragraph."""
        
        chunks = processor.chunk_transcript(content)
        
        # Should create chunks for paragraphs
        assert len(chunks) == 3
        assert chunks[0]['speaker'] == 'Speaker'
        assert 'first paragraph' in chunks[0]['content']
        assert 'second paragraph' in chunks[1]['content']
    
    def test_chunk_transcript_speaker_format(self):
        """Test chunking of speaker-formatted transcript."""
        processor = TextProcessor()
        
        content = """# Interview Transcript

**DHH:** This is what DHH said.
It continues here.

**Interviewer:** This is the interviewer's response.

**DHH:** Another response from DHH."""
        
        chunks = processor.chunk_transcript(content)
        
        # Should create speaker-based chunks
        assert len(chunks) == 3
        assert chunks[0]['speaker'] == 'DHH'
        assert chunks[1]['speaker'] == 'Interviewer'
        assert chunks[2]['speaker'] == 'DHH'
    
    def test_split_large_chunks(self):
        """Test splitting of large chunks into smaller ones."""
        processor = TextProcessor()
        
        chunks = [
            {
                'content': 'First. Second. Third. Fourth. Fifth. Sixth. Seventh. Eighth.',
                'speaker': 'Speaker',
                'original': 'First. Second. Third. Fourth. Fifth. Sixth. Seventh. Eighth.'
            }
        ]
        
        result = processor.split_large_chunks(chunks, max_sentences=3)
        
        # Should split into multiple chunks
        assert len(result) >= 2
        assert result[0]['speaker'] == 'Speaker'