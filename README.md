# yt-aprtr

A powerful tool designed for Claude Code and AI agents to extract YouTube subtitles and perform semantic search over video content using state-of-the-art language models.

> **Built for AI Analysis**: This repository is specifically designed to be used with Claude Code or other AI agents to read, analyze, and explore YouTube video content through natural language queries.

## Features

**AI-First Design**
- Built for Claude Code and AI agents to analyze video content
- Natural language interface perfect for AI-driven exploration
- Structured output optimized for AI consumption

**YouTube Subtitle Extraction**
- Extract subtitles from any YouTube video
- Support for multiple languages
- Automatic cleaning and formatting
- VTT to clean text conversion

**Semantic Search for AI Analysis**
- Natural language search over transcript content
- Powered by sentence transformers for AI understanding
- Cosine similarity ranking with contextual results
- Expandable context viewing for deep analysis

**Performance Optimized**
- Embedding caching for fast repeated searches
- Batch processing for large transcripts
- Efficient chunking strategies

**Developer Friendly**
- Clean modular architecture
- Comprehensive CLI interface
- Environment-based configuration
- Type hints and documentation

## Quick Start for Claude Code & AI Agents

### Setup for AI Analysis

```bash
# Clone and setup for Claude Code
git clone https://github.com/your-org/yt-aperture
cd yt-aperture

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .

# Now your AI agent can analyze any YouTube video content
```

## Usage for AI Analysis

### Perfect for Claude Code Workflows

This tool is designed to work seamlessly with Claude Code and other AI agents. Here are the key workflows:

### Extract Subtitles for AI Analysis
```bash
# Extract subtitles from any YouTube video for AI analysis
./yt-aprtr extract "https://youtube.com/watch?v=abc123" -n my_video

# Extract with custom language for multilingual analysis
./yt-aprtr extract "https://youtube.com/watch?v=abc123" -l es -n spanish_video
```

### AI-Optimized Semantic Search
```bash
# Search transcripts using natural language - perfect for AI queries
./yt-aprtr search "artificial intelligence" -t transcript.txt -r 10

# Expand specific results with full context for deeper AI analysis
./yt-aprtr search "consciousness" -t transcript.txt --expand 45 --context 5
```

### One-Step Extract & Analyze
```bash
# Extract and immediately search - ideal for AI-driven exploration
./yt-aprtr auto "https://youtube.com/watch?v=abc123" "neural networks" -n interview -r 15
```

## Command Line Arguments

### Extract Command
- `url`: YouTube video URL (required)
- `-l, --language`: Subtitle language code (default: en)
- `-n, --name`: Custom output filename
- `-o, --output-dir`: Output directory (default: current)

### Search Command
- `query`: Search query (required for search mode)
- `-t, --transcript`: Transcript file path (required)
- `-r, --results`: Number of results (default: 10)
- `-e, --expand`: Expand specific result ID
- `-c, --context`: Context chunks for expand (default: 3)

### Auto Command (Extract + Search)
- `url`: YouTube video URL (required)
- `query`: Search query (required)
- `-l, --language`: Subtitle language code (default: en)
- `-n, --name`: Custom output filename
- `-o, --output-dir`: Output directory (default: current)
- `-r, --results`: Number of results (default: 10)

## Examples

### Extract YouTube Videos
```bash
./yt-aprtr extract "https://youtube.com/watch?v=dQw4w9WgXcQ" -n rick_roll
./yt-aprtr extract "https://youtube.com/watch?v=abc123" -l fr -n french_interview
```

### Search Content
```bash
./yt-aprtr search "machine learning algorithms" -t extractions/interview/interview.en.txt -r 15
./yt-aprtr search "startup advice" -t transcript.md --expand 123 --context 4
```

### One-Step Extract and Search
```bash
./yt-aprtr auto "https://youtube.com/watch?v=abc123" "artificial intelligence" -n ai_talk -r 20
```

## AI-Optimized Workflow

1. **Extract**: Use Claude Code to extract subtitles from any YouTube video
2. **Search**: Ask AI to search transcripts using natural language queries
3. **Discover**: Let AI discover relevant content through semantic understanding
4. **Analyze**: Expand interesting results for deeper AI-driven analysis
5. **Synthesize**: Use AI to synthesize insights across multiple video sources

## Sample Output

### Search Results
```
Searching for: 'Ruby on Rails'
Results: 10

Found 10 results:

[245] DHH (Score: 0.832)
    Ruby on Rails is a web development framework I created. It's designed to make programming web applications easier and more enjoyable.

[387] DHH (Score: 0.798)
    The philosophy behind Rails is convention over configuration. We make decisions so developers don't have to make them repeatedly.

[512] DHH (Score: 0.776)
    Rails has been used to build millions of applications including Shopify and GitHub. That's incredibly gratifying to see.

Perfect for AI Analysis: Use --expand [ID] to get full context for Claude Code or other AI agents
Example: ./yt-aprtr search "query" -t transcript.txt --expand 123 --context 3
```

### Expanded Context
```
Expanding result ID: 245
Context paragraphs: 3

======================================================================
**DHH:** The satisfaction of driving a race car is driving it at the edge of adhesion, as we call it, where you're essentially just a tiny movement away from spinning out. That balance of danger and skill is what's so intoxicating.

**Interviewer:** For someone who became a legendary programmer, you officially got into programming late in life. Can you tell me about your journey?

>>> MAIN RESULT <<<
**DHH:** Ruby on Rails is a web development framework I created. It's designed to make programming web applications easier and more enjoyable. The philosophy behind Rails is convention over configuration - we make decisions so developers don't have to make them repeatedly.
>>> END RESULT <<<

**DHH:** This approach has allowed millions of developers to build applications faster and with less complexity. It's been used for everything from small personal projects to massive applications like Shopify and GitHub.

**Interviewer:** What inspired you to create Rails in the first place?
======================================================================
```

## How It Works

1. **Chunking**: The transcript is split into paragraph-level chunks
2. **Embedding**: Each chunk is converted to a vector representation using sentence transformers
3. **Similarity**: Your query is embedded and compared to all chunks using cosine similarity
4. **Snippets**: Brief 2-sentence previews are extracted from matches
5. **Expansion**: Full context with surrounding paragraphs available on demand
6. **Caching**: Embeddings are cached locally to speed up future searches

## Files

- `yt-aprtr`: Main CLI entry point
- `src/`: Source code directory
  - `core/`: Core functionality (extractor, searcher, processor, cache)
  - `cli/`: Command line interface
  - `config/`: Configuration settings
- `pyproject.toml`: Modern Python packaging configuration
- `requirements.txt`: Python dependencies
- `README.md`: This documentation
- `extractions/`: Directory containing extracted YouTube subtitles (created on first extraction)
- `cache/`: Directory containing cached embeddings (created on first search)
- `venv/`: Virtual environment directory

## Tips for AI-First Analysis

- **Use natural language queries** - perfect for AI-driven exploration
- **Let AI discover patterns** through semantic understanding
- **Expand results for Claude Code** to get full context for analysis
- **Try conversational queries** that mirror how you'd ask an AI
- **Leverage similarity scores** to help AI gauge relevance
- **Use auto command** for streamlined AI workflows
- **Synthesize insights** across multiple videos using AI analysis

## Technical Details

- Uses the `all-MiniLM-L6-v2` sentence transformer model
- Embeddings are 384-dimensional vectors
- Cosine similarity is used for ranking
- Results include similarity scores (0-1 scale)
- First run creates ~3000 embeddings for the transcript chunks
- Subsequent searches are near-instantaneous thanks to caching 