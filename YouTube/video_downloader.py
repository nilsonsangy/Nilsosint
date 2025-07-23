import os
import sys
import yt_dlp

# Check if video URL is passed as a command-line argument
def is_valid_youtube_url(url):
    # Basic validation for YouTube URLs
    return url.startswith("https://www.youtube.com/") or url.startswith("https://youtu.be/")

if len(sys.argv) > 1:
    url = sys.argv[1].strip()
else:
    url = input("Enter the YouTube video URL: ").strip()

if not url:
    print("Error: No URL provided. Please enter a valid YouTube video URL.")
    sys.exit(1)

if not is_valid_youtube_url(url):
    print("Error: The provided URL is not a valid YouTube link.")
    sys.exit(1)

# Get user's Desktop path
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Set yt-dlp options
ydl_opts = {
    'outtmpl': os.path.join(desktop_path, '%(title)s.%(ext)s'),
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4',
    'quiet': False
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print(f"Download completed! Video saved to {desktop_path}")