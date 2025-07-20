# YouTube Video Downloader

This tool downloads YouTube videos directly to your Desktop using yt-dlp.

## Usage

1. Make sure yt-dlp and ffmpeg are installed (see root requirements and instructions).
   - Download ffmpeg: [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)
   - After downloading, extract and add the `bin` folder to your PATH, or copy `ffmpeg.exe` to a folder in your PATH (e.g., `C:\Windows\System32`).
2. Run the script:
   ```powershell
   python video_downloader.py [YouTube_URL]
   ```
   - You can provide the video URL as a command-line argument, or the script will prompt you for it.

## Requirements
- Python 3.11
- yt-dlp (installed via requirements.txt)
- ffmpeg (must be installed and in your PATH)

## Output
- The downloaded video will be saved to your Desktop with the original YouTube title.
