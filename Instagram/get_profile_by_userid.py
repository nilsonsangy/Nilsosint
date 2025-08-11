

import requests
import os
import json

COOKIES_FILE = os.path.join(os.path.dirname(__file__), 'instagram_cookies.txt')

def load_cookies_from_txt(path):
    """
    Loads cookies from a text file exported from browser dev tools.
    Returns a dict suitable for requests.
    """
    cookies = {}
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            # Skip empty or invalid lines
            if not line.strip() or line.startswith('#') or line.strip() == 'wd':
                continue
            try:
                if '\t' in line:
                    # Netscape format (tab-separated)
                    parts = line.strip().split('\t')
                    if len(parts) >= 7:
                        key = parts[5]
                        value = parts[6]
                        # Remove non-ASCII characters from value
                        value = value.encode('ascii', errors='ignore').decode('ascii')
                        cookies[key] = value
                elif '=' in line:
                    # Simple key=value
                    key, value = line.strip().split('=', 1)
                    value = value.encode('ascii', errors='ignore').decode('ascii')
                    cookies[key] = value
            except Exception as e:
                print(f"Skipping line due to error: {e}")
                continue
    return cookies

def get_instagram_profile(user_id):
    """
    Given an Instagram user_id, returns the username and profile link using authenticated cookies.
    """
    cookies = load_cookies_from_txt(COOKIES_FILE)
    # Use only cookies that exist in the file
    headers = {
        "User-Agent": "Instagram 155.0.0.37.107 Android (30/11; 320dpi; 720x1280; Xiaomi; Redmi Note 7; lavender; qcom; en_US)",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "X-IG-App-ID": "936619743392459",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/",
    }
    url = f"https://i.instagram.com/api/v1/users/{user_id}/info/"
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        try:
            data = response.json()
            username = data['user']['username']
            profile_url = f"https://instagram.com/{username}"
            return username, profile_url
        except Exception as e:
            print(f"Error parsing response: {e}")
            print(f"Raw response: {response.text}")
            return None, None
    else:
        print(f"Failed to fetch profile. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None, None

if __name__ == "__main__":
    user_id = input("Enter the Instagram user_id: ")
    username, profile_url = get_instagram_profile(user_id)
    if username and profile_url:
        print(f"Username: {username}")
        print(f"Profile link: {profile_url}")
    else:
        print("Could not get the username from user_id. Check your cookies or user_id.")
