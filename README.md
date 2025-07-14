# NilScan
NilScan is a collection of open-source tools and scripts for OSINT (Open Source Intelligence), focused on digital footprinting, data collection, and target reconnaissance.

## How to set up the Python environment

You can set up the environment automatically using the provided PowerShell script, or manually if you prefer.

### Option 1: Automatic setup (recommended)

Run the setup script in PowerShell:
```powershell
./setup.ps1
```
This script will:
- Check if Python 3.8 or newer is installed. If not, it will prompt you to install it.
- Create and activate a virtual environment.
- Upgrade pip.
- Install all required packages from requirements.txt.

### Option 2: Manual setup

1. Create and activate the virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
2. Install the dependencies:
   ```powershell
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```
   > **Note:** If you encounter an error related to compiling packages, ensure you have a compatible Python version (3.8+ recommended) and pip is up to date.

## Environment variables and API credentials

This project uses a `.env` file to store your X (Twitter) API credentials securely. The `.env` file should not be committed to version control (see `.gitignore`).

1. Copy `.env-example` to `.env`:
   ```powershell
   cp .env-example .env
   ```
2. Fill in your API credentials in the `.env` file:
   - `API_KEY`
   - `API_SECRET`
   - `BEARER_TOKEN`
   - `ACCESS_TOKEN`
   - `ACCESS_TOKEN_SECRET`

The application will automatically load these credentials using `python-dotenv` and use them to authenticate with the X API via Tweepy.

## Package descriptions

- **snscrape**: Twitter scraping tool that works without API keys and is actively maintained.
- **pandas**: Data analysis and manipulation library.
- **spacy**: Industrial-strength Natural Language Processing (NLP) library.
- **matplotlib**: Comprehensive library for creating static, animated, and interactive visualizations in Python.
- **networkx**: Library for the creation, manipulation, and study of complex networks and graphs.
- **bertopic**: Topic modeling tool that leverages transformers and c-TF-IDF to create easily interpretable topics.
- **transformers**: State-of-the-art machine learning library for natural language processing, including pretrained models like BERT.
- **en_core_web_sm**: spaCy's small English language model for NLP tasks.
