<div align="center">

# 🕵️‍♂️ Nilsosint

**A powerful toolkit for Open Source Intelligence (OSINT), digital footprinting, and data collection**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)](https://github.com/nilsonsangy/Nilsosint)

*Empowering researchers, investigators, and enthusiasts with automated OSINT tools*

</div>

---

## 📋 Table of Contents

- [🛠️ Tools Overview](#️-tools-overview)
- [🚀 Quick Start](#-quick-start)
- [🔧 Installation](#-installation)
- [📖 Usage](#-usage)
  - [Instagram User Lookup](#instagram-user-lookup)
  - [X (Twitter) Analysis](#x-twitter-analysis)
  - [YouTube Video Downloader](#youtube-video-downloader)
- [⚙️ Requirements](#️-requirements)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [⚠️ Disclaimer](#️-disclaimer)
- [📞 Contact](#-contact)

---

## 🛠️ Tools Overview

| Tool                      | Description                                      | Input                | Output                | Use Case                |
|---------------------------|--------------------------------------------------|----------------------|-----------------------|-------------------------|
| **Instagram User Lookup** | Get username and profile link from user ID       | Instagram user ID    | Username, profile URL | OSINT, investigations   |
| **X (Twitter) Analysis**  | Collect tweets, analyze sentiment, topics, NER   | Twitter username     | CSV, graphs, analysis | Social media research   |
| **YouTube Downloader**    | Download YouTube videos with yt-dlp              | Video URL            | Video file            | Evidence collection     |

---

## 🚀 Quick Start

```powershell
# Clone the repository
git clone https://github.com/nilsonsangy/Nilsosint.git
cd Nilsosint

# Run the setup script (recommended)
./setup.ps1
```

Or set up manually (see Installation).

---

## 🔧 Installation

### Prerequisites

- **Python 3.x** (any recent version)
- **pip** (Python package manager)
- **ffmpeg** (for YouTube downloads, optional but recommended)

### Automated Setup (Recommended)

You can use the script below to automate all steps:

```powershell
./enable_python_environment.ps1
```
This script will:
- Check if Python is installed (and install the latest version if not)
- Create and activate a virtual environment
- Upgrade pip
- Install all required packages from requirements.txt
- Download the spaCy English model

### Manual Setup

If you prefer to do it manually:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

## 📖 Usage

### Instagram User Lookup

Get the username and profile link from an Instagram user ID using your own session cookies.

```powershell
python Instagram/get_profile_by_userid.py
```
- Follow the instructions in [`Instagram/HOW_TO_EXPORT_INSTAGRAM_COOKIES.md`](Instagram/HOW_TO_EXPORT_INSTAGRAM_COOKIES.md) to export your cookies safely.

### X (Twitter) Analysis

Collect and analyze tweets, perform sentiment analysis, topic modeling, and build mention networks.

```powershell
python X/collect_tweets.py
```
- Requires X (Twitter) API credentials in a `.env` file. See `.env-example` for details.

### YouTube Video Downloader

Download YouTube videos directly to your desktop.

```powershell
python YouTube/video_downloader.py
```
- Requires `yt-dlp` and `ffmpeg` for best results.

---

## ⚙️ Requirements

- **Operating System**: Windows, Linux, or macOS
- **Python**: 3.7 or higher
- **pip**: Latest version recommended
- **ffmpeg**: For YouTube downloads

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

Please follow code style conventions and add documentation for new features.

---

## 📄 License

---

## 💝 Donations

If you find this project helpful and would like to support its development, consider making a donation. Your contribution helps keep this toolkit updated and motivates further improvements!

[![Donate with PayPal](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://www.paypal.com/donate/?business=7CC3CMJVYYHAC&no_recurring=0&currency_code=BRL)

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

This toolkit is for **educational and research purposes only**. Use responsibly and ensure compliance with all applicable laws.

---

## 📞 Contact

- **GitHub Issues**: [Open an issue](https://github.com/nilsonsangy/Nilsosint/issues) for questions or bug reports

<div align="center">

**⭐ If you found this project useful, please give it a star!**

Made with ❤️ for the OSINT community

</div>
