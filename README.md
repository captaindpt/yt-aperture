# YouTube Semantic Search (yt-aperture)

A powerful Python tool for extracting YouTube subtitles and performing semantic search over video content using state-of-the-art sentence transformer models. Built specifically for AI-assisted video content analysis with Claude Code.

## What It Does

**Extract YouTube Subtitles**: Downloads and cleans subtitles from any YouTube video using yt-dlp, supporting multiple languages and auto-generated captions.

**Semantic Search**: Performs natural language search over transcript content using sentence embeddings and cosine similarity ranking. Find specific topics, concepts, or discussions without exact keyword matching.

**AI-Optimized Workflows**: Designed for Claude Code and AI agents to analyze video content through conversational queries and contextual exploration.

## Key Features

- **Fast Performance**: File-based embedding cache eliminates redundant processing - first search creates embeddings (~3-5s), subsequent searches are near-instant
- **Intelligent Chunking**: Transcripts split into 4-6 sentence segments for optimal search granularity
- **Context Expansion**: View surrounding content for any search result with configurable context windows
- **Multi-format Support**: Works with speaker-formatted transcripts and plain text
- **CLI Interface**: Simple commands for extraction, search, and combined workflows

## Technical Architecture

- **Embedding Model**: `all-MiniLM-L6-v2` sentence transformer (384-dimensional vectors)
- **Search Engine**: Cosine similarity ranking with semantic understanding
- **Caching System**: Per-transcript embedding cache with file modification validation
- **Text Processing**: Intelligent chunking and snippet extraction for various transcript formats

## Installation

```bash
git clone https://github.com/your-org/yt-aperture
cd yt-aperture
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Basic Usage

### Extract Subtitles
```bash
# Extract from YouTube video
./yt-aprtr extract "https://youtube.com/watch?v=VIDEO_ID" -n my_video

# With custom language
./yt-aprtr extract "https://youtube.com/watch?v=VIDEO_ID" -l es -n spanish_video
```

### Search Content
```bash
# Semantic search
./yt-aprtr search "artificial intelligence" -t transcript.txt -r 10

# Expand specific result with context
./yt-aprtr search "machine learning" -t transcript.txt --expand 42 --context 3
```

### Extract and Search Combined
```bash
# One command workflow
./yt-aprtr auto "https://youtube.com/watch?v=VIDEO_ID" "neural networks" -n interview -r 15
```

## Using with Claude Code

This tool is specifically designed for AI-assisted analysis. Launch Claude Code in the repository directory:

```bash
cd yt-aperture
claude-code
```

Claude Code can then:
- Extract subtitles from any YouTube video you provide
- Search transcript content using natural language queries
- Analyze themes, extract insights, and synthesize findings
- Create structured analysis reports in markdown format

**AI Instructions**: Claude Code will automatically read [`CLAUDE.md`](./CLAUDE.md) for detailed usage patterns, command examples, and analysis workflows optimized for AI agents.

## Sample Output

```
🔍 Searching for: 'startup advice'

🎯 Found 10 results:

[156] Speaker (Score: 0.847)
    The most important thing for early-stage startups is to focus on product-market fit before anything else.

[203] Speaker (Score: 0.792)
    Don't scale your team until you've validated that people actually want what you're building.

[089] Speaker (Score: 0.761)
    Talking to customers daily is not optional - it's the difference between success and failure.

💡 Use --expand [ID] to see full context around a specific result
```

Expand for full context:
```bash
./yt-aprtr search "startup advice" -t transcript.txt --expand 156 --context 2
```

## Performance Characteristics

- **First Search**: Downloads sentence transformer model (~90MB), creates embeddings for transcript chunks
- **Subsequent Searches**: Uses cached embeddings for near-instant results
- **Memory Usage**: ~2GB RAM recommended for model loading
- **Cache Storage**: ~5MB per transcript for embeddings and chunks

## Project Structure

```
yt-aperture/
├── src/core/           # Core functionality (extractor, searcher, processor, cache)
├── extractions/        # Extracted video transcripts (auto-created)
├── cache/             # Embedding cache storage (auto-created)
├── yt-aprtr           # Main executable script
├── CLAUDE.md          # AI agent instructions and technical examples
├── pyproject.toml     # Python packaging configuration
└── requirements.txt   # Dependencies
```

## Dependencies

- **yt-dlp**: YouTube video/subtitle downloading
- **sentence-transformers**: Semantic embedding generation  
- **scikit-learn**: Cosine similarity calculations
- **numpy**: Numerical operations
- **torch**: PyTorch backend for transformers

## Configuration

Set environment variables to customize behavior:
```bash
export YSS_MODEL_NAME="all-MiniLM-L6-v2"  # Sentence transformer model
export YSS_CACHE_DIR="cache"              # Cache directory
export YSS_DEFAULT_RESULTS="10"           # Default number of results
```

## Development

```bash
# Run tests
pytest tests/

# Code formatting
black src/ tests/

# Type checking  
mypy src/
```

## License

MIT License - see LICENSE file for details.