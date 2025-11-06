import os
import sys
from typing import Optional, Tuple

from dotenv import load_dotenv
import yt_dlp


def is_valid_youtube_url(url: str) -> bool:
    """Basic validation for YouTube URLs."""
    return url.startswith("https://www.youtube.com/") or url.startswith("https://youtu.be/")


def build_base_opts(download_dir: str) -> dict:
    """Common yt-dlp options for best quality MP4 output on Desktop."""
    return {
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': False,
    }


def get_cookies_from_env() -> Tuple[Optional[str], Optional[Tuple]]:
    """Read cookies configuration from environment variables.

    Returns a tuple (cookiefile, cookiesfrombrowser_tuple)
    Only one of them will be non-None if configured.
    """
    cookiefile = os.getenv('YT_COOKIES_FILE')
    browser = os.getenv('YT_COOKIES_BROWSER')
    profile = os.getenv('YT_COOKIES_PROFILE')

    cookiesfrombrowser = None
    if browser:
        browser = browser.strip().lower()
        # yt-dlp expects a tuple, profile is optional
        if profile and profile.strip():
            cookiesfrombrowser = (browser, profile.strip())
        else:
            cookiesfrombrowser = (browser,)

    if cookiefile and cookiefile.strip():
        cookiefile = os.path.expanduser(os.path.expandvars(cookiefile.strip()))

    return cookiefile, cookiesfrombrowser


def analyze_cookie_file(path: str) -> Tuple[int, int, int, bool]:
    """Return simple diagnostics about the cookies.txt file.

    Returns: (total_lines, youtube_lines, accounts_lines, has_core_auth_cookies)
    has_core_auth_cookies is True if we detect likely login-related cookie names.
    """
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        youtube_lines = sum(1 for l in lines if 'youtube.com' in l)
        accounts_lines = sum(1 for l in lines if 'accounts.google.com' in l)
        # Look for key auth cookie names (case-insensitive match in lines)
        marker_names = ('SID', 'SAPISID', 'HSID', 'SSID', 'LOGIN_INFO', 'PREF', 'CONSENT')
        has_core = any(any(m in l for m in marker_names) for l in lines)
        return len(lines), youtube_lines, accounts_lines, has_core
    except Exception:
        return 0, 0, 0, False


def print_auth_help() -> None:
    """Explain how to configure authentication for YouTube downloads.

    Important: YouTube Data API keys cannot authenticate video downloads; you must
    provide cookies from a logged-in browser session. The API key is optional and
    only useful for metadata tasks (not used by this downloader).
    """
    help_text = f"""
Authentication required by YouTube
---------------------------------
Some videos require you to be signed in (e.g., "Sign in to confirm you're not a bot").
To allow downloads in these cases, configure ONE of the options below in your .env file:

1) Use cookies-from-browser (recommended)
   - Add these entries to .env (create it from .env-example if needed):
       YT_COOKIES_BROWSER=chrome   # or edge | firefox | brave | vivaldi | opera
       YT_COOKIES_PROFILE=Default  # optional; e.g., "Default", "Profile 1"

   The downloader will securely read cookies directly from your installed browser.

2) Use an exported cookies file
   - Export cookies for youtube.com (e.g., with the "Get cookies.txt LOCALLY" browser extension)
   - Save the exported file and set in .env:
       YT_COOKIES_FILE=C:\\path\\to\\cookies.txt

About API keys (YT_DATA_API_KEY)
--------------------------------
An API key for "YouTube Data API v3" CANNOT authenticate downloads or bypass the
"sign in" check. It is only for metadata queries. If you still want to create one:
 - Go to Google Cloud Console -> Create Project -> Enable APIs & Services
 - Enable: "YouTube Data API v3"
 - Go to "APIs & Services > Credentials" -> "Create credentials" -> "API key"
 - Add to .env:
       YT_DATA_API_KEY=your_api_key_here

After updating .env, run the downloader again.
"""
    print(help_text)


def try_download(url: str, opts: dict) -> bool:
    """Attempt a download with given options. Return True if successful."""
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        return True
    except yt_dlp.utils.DownloadError as e:
        # Bubble up specific message for auth-required cases
        err = str(e)
        # Common markers when authentication is required
        auth_markers = (
            "Sign in to confirm you’re not a bot",
            "This video is only available for registered users",
            "login required",
        )
        if any(m in err for m in auth_markers):
            raise PermissionError(err) from e
        # Re-raise other errors so they're visible
        raise


def main():
    # Acquire URL from args or input
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

    # Download to Desktop by default
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    base_opts = build_base_opts(desktop_path)

    # First attempt: without any authentication
    try:
        if try_download(url, base_opts):
            print(f"Download completed! Video saved to {desktop_path}")
            return
    except PermissionError:
        # Continue to authenticated attempt
        pass

    # Second attempt: with cookies from .env (browser or cookiefile)
    print("YouTube requires authentication for this video. Checking .env for cookies settings…")
    load_dotenv()  # Load once when needed
    cookiefile, cookiesfrombrowser = get_cookies_from_env()

    authed_opts = dict(base_opts)
    used_auth = None

    if cookiefile and os.path.isfile(cookiefile):
        # Diagnose cookie file quality before attempting
        total_lines, yt_lines, acc_lines, has_core = analyze_cookie_file(cookiefile)
        if yt_lines < 5 or not has_core:
            print("[Warning] The cookies.txt file may be incomplete for authenticated YouTube access.")
            print(f"          Total lines: {total_lines}, youtube.com lines: {yt_lines}, accounts.google.com lines: {acc_lines}")
            print("          Key auth cookie names present:" if has_core else "          Missing key auth cookie names (SID/SAPISID/LOGIN_INFO/CONSENT).")
            print("          Try re-exporting after opening https://www.youtube.com while logged in (not in Incognito).")
            print("          Alternative: generate cookies via yt-dlp directly:")
            print("          yt-dlp --cookies-from-browser chrome --dump-cookies new_cookies.txt")
        authed_opts['cookiefile'] = cookiefile
        used_auth = f"cookie file: {cookiefile}"
    elif cookiesfrombrowser:
        authed_opts['cookiesfrombrowser'] = cookiesfrombrowser
        used_auth = f"browser cookies: {cookiesfrombrowser[0]}" + (f" / profile: {cookiesfrombrowser[1]}" if len(cookiesfrombrowser) > 1 else "")
    else:
        print_auth_help()
        sys.exit(2)

    try:
        if try_download(url, authed_opts):
            print(f"Download completed using {used_auth}! Video saved to {desktop_path}")
            return
    except Exception as e:
        err = str(e)
        # If Chromium-based browser cookie DB is locked by a running process, yt-dlp may fail to copy it
        if cookiesfrombrowser and 'Could not copy Chrome cookie database' in err:
            # If a cookies.txt was also provided, try falling back to it automatically
            if cookiefile and os.path.isfile(cookiefile):
                print("Browser cookie database is locked. Falling back to cookies.txt file…")
                fallback_opts = dict(base_opts)
                fallback_opts['cookiefile'] = cookiefile
                if try_download(url, fallback_opts):
                    print(f"Download completed using cookie file: {cookiefile}! Video saved to {desktop_path}")
                    return
            # Otherwise, give targeted guidance
            print("Authenticated download failed: browser cookie database is locked or cannot be copied.")
            print("Fix suggestions:")
            print(" - Close your browser completely (Chrome/Brave/Edge), including background processes.")
            print("   In Chromium-based browsers: Settings > System > disable 'Continue running background apps when closed'.")
            print(" - Ensure no chrome.exe/brave.exe/msedge.exe are running in Task Manager.")
            print(" - Try again, or export cookies to a cookies.txt file and set YT_COOKIES_FILE in .env.")
            print("   See: https://github.com/yt-dlp/yt-dlp/issues/7271")
            sys.exit(3)

        # If Windows DPAPI decryption fails (Chromium cookies), suggest cookies.txt or different browser
        if cookiesfrombrowser and 'Failed to decrypt with DPAPI' in err:
            if cookiefile and os.path.isfile(cookiefile):
                print("Windows DPAPI decryption failed. Falling back to cookies.txt file…")
                fallback_opts = dict(base_opts)
                fallback_opts['cookiefile'] = cookiefile
                if try_download(url, fallback_opts):
                    print(f"Download completed using cookie file: {cookiefile}! Video saved to {desktop_path}")
                    return
            print("Authenticated download failed: Windows could not decrypt browser cookies (DPAPI).")
            print("Fix suggestions:")
            print(" - Run the terminal as the same Windows user that uses the browser (avoid different user contexts).")
            print(" - Try non-elevated (or elevated) PowerShell if the opposite is currently used.")
            print(" - Verify the correct browser profile (e.g., Default vs Profile 1).")
            print(" - Alternatively, export cookies to cookies.txt and set YT_COOKIES_FILE in .env.")
            print("   See: https://github.com/yt-dlp/yt-dlp/issues/10927")
            sys.exit(3)

        print("Authenticated download failed.")
        print(err)
        print()
        print_auth_help()
        sys.exit(3)


if __name__ == "__main__":
    main()