# YouTube Video Downloader

This tool downloads YouTube videos directly to your Desktop using yt-dlp.

## Requirements

- Python 3.11
- yt-dlp (installed via requirements.txt)
- python-dotenv (installed via requirements.txt)
- ffmpeg (must be installed and in your PATH)

Install ffmpeg (Windows):
- Download: https://www.gyan.dev/ffmpeg/builds/
- Extract and add the `bin` folder to your PATH, or copy `ffmpeg.exe` to a folder already in PATH (e.g., `C:\\Windows\\System32`).

## Usage

```powershell
python .\YouTube\video_downloader.py [YouTube_URL]
```
- You can provide the video URL as a command-line argument, or the script will prompt you for it.
- The video will be saved to your Desktop with the original YouTube title.

## Handling authentication-required videos

Some videos prompt: “Sign in to confirm you’re not a bot” or otherwise require login. API keys do not authenticate downloads. Use one of the cookie methods below via `.env`.

1) Cookies from your installed browser (recommended)
- Copy `.env-example` to `.env` at the project root.
- Add this to your `.env` (adjust browser/profile as needed):

  ```env
  YT_COOKIES_BROWSER=chrome   # or edge | firefox | brave | vivaldi | opera
  YT_COOKIES_PROFILE=Default  # optional; e.g., "Default", "Profile 1"
  ```

- The downloader will read cookies directly from your browser profile.

2) Exported cookies.txt file
- Export cookies for youtube.com using a browser extension (e.g., “Get cookies.txt LOCALLY”).
- Save the file (e.g., `C:\\Users\\<you>\\Downloads\\cookies.txt`) and add to `.env`:

  ```env
  YT_COOKIES_FILE=C:\\Users\\<you>\\Downloads\\cookies.txt
  ```

When a download needs authentication, the script will first try without auth, then automatically try cookies based on your `.env`. If no cookies are configured, it prints a help message explaining how to set them up.

## About YouTube API keys (YT_DATA_API_KEY)

A YouTube Data API v3 “API key” cannot be used to authenticate downloads or bypass the “sign in” prompt. It’s only for querying metadata (e.g., channel/video info) and is not used by this downloader. If you still want to create one for other tooling:

### How to create a YouTube Data API v3 API key
1. Go to https://console.cloud.google.com/ and sign in.
2. Create a new Project (top bar Project selector -> New Project) or select an existing one.
3. In the left menu, open “APIs & Services” -> “Library”.
4. Search for “YouTube Data API v3” and click “Enable”.
5. Go to “APIs & Services” -> “Credentials”.
6. Click “Create credentials” -> “API key”.
7. Copy the generated key and add to your `.env` file:

   ```env
   YT_DATA_API_KEY=your_api_key_here
   ```

Again: this key will NOT help with authentication for downloads; use cookies as described above.

## Troubleshooting

- "Could not copy Chrome cookie database"
  - Close the browser completely (including background processes).
  - In Chromium-based browsers (Chrome/Brave/Edge): Settings > System > disable "Continue running background apps when closed".
  - Ensure no browser processes are running in Task Manager.
  - Optionally, export cookies to a cookies.txt file and set `YT_COOKIES_FILE` in `.env`.

- "Failed to decrypt with DPAPI" (Windows)
  - Run the terminal as the same Windows user that uses the browser.
  - Try the opposite elevation (non-admin vs admin) if you still see errors.
  - Verify the correct browser profile name (e.g., `Default`, `Profile 1`).
  - As a reliable fallback, export cookies to a `cookies.txt` and set `YT_COOKIES_FILE` in `.env`.
