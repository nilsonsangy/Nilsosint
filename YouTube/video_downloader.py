import os
import sys
import yt_dlp

# Check if video URL is passed as a command-line argument
if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    url = input("Enter the YouTube video URL: ")

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