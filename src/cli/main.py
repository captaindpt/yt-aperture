"""Main CLI interface for YouTube Semantic Search."""

import argparse
import sys
from pathlib import Path
from typing import Optional

from ..core.extractor import YouTubeExtractor
from ..core.searcher import SemanticSearcher
from ..config.settings import default_config


def extract_command(args):
    """Handle extract subcommand."""
    extractor = YouTubeExtractor(args.output_dir)
    
    try:
        vtt_file, text_file = extractor.extract_subtitles(
            args.url,
            args.language,
            args.name
        )
        print(f"✅ Extraction complete:")
        print(f"   VTT file: {vtt_file}")
        print(f"   Text file: {text_file}")
        
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        sys.exit(1)


def search_command(args):
    """Handle search subcommand."""
    if not Path(args.transcript).exists():
        print(f"❌ Transcript file not found: {args.transcript}")
        print("Available files:")
        for file in Path(".").iterdir():
            if file.suffix in ['.md', '.txt']:
                print(f"  - {file}")
        sys.exit(1)
    
    # Create searcher
    searcher = SemanticSearcher(
        model_name=default_config.search.model_name,
        cache_dir=default_config.search.cache_dir
    )
    
    try:
        searcher.load_transcript(args.transcript)
        
        # Handle expand mode
        if args.expand is not None:
            print(f"🔍 Expanding result ID {args.expand} with {args.context} chunks of context:")
            print("=" * 70)
            expanded_context = searcher.get_expanded_context(args.expand, args.context)
            print(expanded_context)
            print("=" * 70)
            return
        
        # Handle search mode
        if not args.query:
            print("❌ Please provide a search query")
            sys.exit(1)
        
        # Perform search
        results = searcher.search(args.query, args.results)
        searcher.print_results(results)
        
    except Exception as e:
        print(f"❌ Search failed: {e}")
        sys.exit(1)


def extract_and_search_command(args):
    """Handle combined extract and search."""
    # First extract
    print("🎬 Extracting subtitles from YouTube...")
    extractor = YouTubeExtractor(args.output_dir)
    
    try:
        _, text_file = extractor.extract_subtitles(
            args.url,
            args.language,
            args.name
        )
        
        # Then search
        print(f"\n🔍 Searching for: {args.query}")
        searcher = SemanticSearcher(
            model_name=default_config.search.model_name,
            cache_dir=default_config.search.cache_dir
        )
        
        searcher.load_transcript(text_file)
        results = searcher.search(args.query, args.results)
        searcher.print_results(results)
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="YouTube Semantic Search - Extract and search YouTube subtitles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract subtitles from YouTube video
  yss extract https://youtube.com/watch?v=abc123 -n my_video

  # Search existing transcript
  yss search "artificial intelligence" -t transcript.txt -r 10

  # Extract and search in one command
  yss auto https://youtube.com/watch?v=abc123 "AI consciousness" -n interview

  # Expand context around specific result
  yss search "consciousness" -t transcript.txt --expand 45 --context 5
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract subtitles from YouTube')
    extract_parser.add_argument('url', help='YouTube video URL')
    extract_parser.add_argument('-l', '--language', default='en', help='Subtitle language (default: en)')
    extract_parser.add_argument('-n', '--name', help='Output filename (auto-generated if not provided)')
    extract_parser.add_argument('-o', '--output-dir', default='.', help='Output directory (default: current)')
    extract_parser.set_defaults(func=extract_command)
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search existing transcript')
    search_parser.add_argument('query', nargs='?', help='Search query')
    search_parser.add_argument('-t', '--transcript', required=True, help='Transcript file path')
    search_parser.add_argument('-r', '--results', type=int, default=10, help='Number of results (default: 10)')
    search_parser.add_argument('-e', '--expand', type=int, help='Expand specific result ID')
    search_parser.add_argument('-c', '--context', type=int, default=3, help='Context chunks for expand (default: 3)')
    search_parser.set_defaults(func=search_command)
    
    # Auto command (extract + search)
    auto_parser = subparsers.add_parser('auto', help='Extract and search in one command')
    auto_parser.add_argument('url', help='YouTube video URL')
    auto_parser.add_argument('query', help='Search query')
    auto_parser.add_argument('-l', '--language', default='en', help='Subtitle language (default: en)')
    auto_parser.add_argument('-n', '--name', help='Output filename (auto-generated if not provided)')
    auto_parser.add_argument('-o', '--output-dir', default='.', help='Output directory (default: current)')
    auto_parser.add_argument('-r', '--results', type=int, default=10, help='Number of results (default: 10)')
    auto_parser.set_defaults(func=extract_and_search_command)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    args.func(args)


if __name__ == "__main__":
    main()