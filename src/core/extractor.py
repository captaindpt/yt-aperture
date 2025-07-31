"""YouTube subtitle extraction functionality."""

import os
import re
import subprocess
from pathlib import Path
from typing import Optional, Tuple


class YouTubeExtractor:
    """Extracts subtitles from YouTube videos."""
    
    def __init__(self, output_dir: str = "."):
        self.base_output_dir = Path(output_dir)
        self.extractions_dir = self.base_output_dir / "extractions"
        self.extractions_dir.mkdir(exist_ok=True)
    
    def extract_subtitles(
        self, 
        url: str, 
        language: str = "en",
        output_name: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Extract subtitles from YouTube video.
        
        Args:
            url: YouTube video URL
            language: Subtitle language code (default: "en")
            output_name: Custom output filename (without extension)
        
        Returns:
            Tuple of (vtt_file_path, text_file_path)
        
        Raises:
            RuntimeError: If extraction fails
        """
        try:
            # Get video info to generate filename if not provided
            if not output_name:
                info_cmd = [
                    "yt-dlp", 
                    "--get-title", 
                    "--get-id", 
                    url
                ]
                result = subprocess.run(info_cmd, capture_output=True, text=True, check=True)
                lines = result.stdout.strip().split('\n')
                title = lines[0] if lines else "video"
                video_id = lines[1] if len(lines) > 1 else "unknown"
                
                # Clean title for filename
                clean_title = re.sub(r'[^\w\s-]', '', title)
                clean_title = re.sub(r'[-\s]+', '_', clean_title)
                output_name = f"{clean_title}_{video_id}"
            
            # Create subdirectory for this extraction
            self.output_dir = self.extractions_dir / output_name
            self.output_dir.mkdir(exist_ok=True)
            
            vtt_file = self.output_dir / f"{output_name}.{language}.vtt"
            
            # Extract subtitles using yt-dlp
            cmd = [
                "yt-dlp",
                "--write-subs",
                "--write-auto-subs", 
                "--sub-langs", language,
                "--skip-download",
                "--output", str(self.output_dir / f"{output_name}.%(ext)s"),
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            if not vtt_file.exists():
                raise RuntimeError(f"Subtitle extraction failed. VTT file not found: {vtt_file}")
            
            # Convert to clean text
            text_file = self._vtt_to_text(vtt_file)
            
            print(f"✅ Subtitles extracted: {text_file}")
            return str(vtt_file), str(text_file)
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"yt-dlp failed: {e.stderr}")
        except Exception as e:
            raise RuntimeError(f"Extraction failed: {str(e)}")
    
    def _vtt_to_text(self, vtt_file: Path) -> Path:
        """Convert VTT subtitle file to clean text."""
        text_file = vtt_file.with_suffix('.txt')
        
        with open(vtt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove VTT headers and metadata
        lines = content.split('\n')
        text_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Skip VTT headers, timestamps, and positioning
            if (line.startswith('WEBVTT') or 
                line.startswith('NOTE') or
                '-->' in line or
                line.startswith('<') or
                re.match(r'^\d+$', line) or
                re.match(r'^[\d:.,\s\-\>]+$', line) or
                not line):
                continue
            
            # Remove HTML tags and positioning attributes
            line = re.sub(r'<[^>]+>', '', line)
            line = re.sub(r'\{[^}]+\}', '', line)
            
            # Clean up extra whitespace
            line = ' '.join(line.split())
            
            if line and len(line) > 2:  # Only keep substantial lines
                text_lines.append(line)
        
        # Remove consecutive duplicates (common in auto-generated subtitles)
        clean_lines = []
        prev_line = ""
        for line in text_lines:
            if line != prev_line:
                clean_lines.append(line)
                prev_line = line
        
        # Join and save
        clean_text = '\n'.join(clean_lines)
        
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(f"**Transcript extracted from YouTube video**\n\n")
            f.write(clean_text)
        
        return text_file