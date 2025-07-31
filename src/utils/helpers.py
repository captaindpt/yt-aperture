"""Helper utility functions."""

import re
from pathlib import Path
from typing import List


def clean_filename(filename: str) -> str:
    """Clean a string to be safe for use as a filename."""
    # Remove or replace problematic characters
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'[-\s]+', '_', filename)
    return filename.strip('_')


def find_transcript_files(directory: Path = Path(".")) -> List[Path]:
    """Find all transcript files in a directory."""
    transcript_files = []
    
    for pattern in ["*.txt", "*.md"]:
        transcript_files.extend(directory.glob(pattern))
    
    return sorted(transcript_files)


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length with suffix."""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix