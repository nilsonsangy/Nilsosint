# X (Twitter) Analysis Tool

This tool collects tweets using the official X (Twitter) API and performs:
- Sentiment analysis
- Topic modeling
- Named entity recognition (NER)
- User mention network graph visualization

## Usage

1. Ensure you have filled in your `.env` file with your X API credentials.
2. Run the script:
   ```powershell
   python collect_tweets.py
   ```
3. Enter the search term when prompted, or modify the script to use a command-line argument if desired.

## Requirements
- Python 3.11
- All dependencies from the root `requirements.txt`

## Output
- Console output with analysis results
- Network graph visualization
