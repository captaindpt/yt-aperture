# YouTube Semantic Search

A powerful tool for extracting YouTube subtitles and performing semantic search over them using state-of-the-art language models.

## Features

**YouTube Subtitle Extraction**
- Extract subtitles from any YouTube video
- Support for multiple languages
- Automatic cleaning and formatting
- VTT to clean text conversion

**Semantic Search**
- Natural language search over transcript content
- Powered by sentence transformers
- Cosine similarity ranking
- Expandable context viewing

**Performance Optimized**
- Embedding caching for fast repeated searches
- Batch processing for large transcripts
- Efficient chunking strategies

**Developer Friendly**
- Clean modular architecture
- Comprehensive CLI interface
- Environment-based configuration
- Type hints and documentation

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/youtube-semantic-search
cd youtube-semantic-search

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .
```

## Usage

### Extract Subtitles from YouTube
```bash
# Extract subtitles from YouTube video
./yss extract "https://youtube.com/watch?v=abc123" -n my_video

# Extract with custom language
./yss extract "https://youtube.com/watch?v=abc123" -l es -n spanish_video
```

### Search Existing Transcripts
```bash
# Search existing transcript
./yss search "artificial intelligence" -t transcript.txt -r 10

# Expand specific result for full context
./yss search "consciousness" -t transcript.txt --expand 45 --context 5
```

### Extract and Search in One Command
```bash
# Extract and search in one command
./yss auto "https://youtube.com/watch?v=abc123" "neural networks" -n interview -r 15
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
./yss extract "https://youtube.com/watch?v=dQw4w9WgXcQ" -n rick_roll
./yss extract "https://youtube.com/watch?v=abc123" -l fr -n french_interview
```

### Search Content
```bash
./yss search "machine learning algorithms" -t extractions/interview/interview.en.txt -r 15
./yss search "startup advice" -t transcript.md --expand 123 --context 4
```

### One-Step Extract and Search
```bash
./yss auto "https://youtube.com/watch?v=abc123" "artificial intelligence" -n ai_talk -r 20
```

## Workflow

1. **Extract**: Extract subtitles from YouTube videos using `yss extract`
2. **Search**: Search transcripts using `yss search` - Get brief snippets with IDs
3. **Browse**: Review the concise results to find interesting matches
4. **Expand**: Use `--expand [ID]` to get full context for specific results

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

Use --expand [ID] to see full context around a specific result
Example: ./yss search "query" -t transcript.txt --expand 123 --context 3
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

- `yss`: Main CLI entry point
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

## Tips

- **Use descriptive queries** for better semantic matching
- **Browse snippets first** to quickly find relevant content
- **Expand interesting results** to see full context
- **Try different phrasings** if initial results aren't perfect
- **Check similarity scores** to gauge relevance (higher = better match)
- **Use the auto command** to extract and search in one step

## Technical Details

- Uses the `all-MiniLM-L6-v2` sentence transformer model
- Embeddings are 384-dimensional vectors
- Cosine similarity is used for ranking
- Results include similarity scores (0-1 scale)
- First run creates ~3000 embeddings for the transcript chunks
- Subsequent searches are near-instantaneous thanks to caching 