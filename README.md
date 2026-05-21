# 🎵 YouTune: YouTube Playlist & Downloader

YouTune is a Flask-powered web application that allows users to download songs via YouTube URLs, search for tracks directly, and manage them in a Spotify-style playlist. With a focus on simplicity and user experience, YouTune bridges the gap between YouTube's vast library and your personal offline collection.

## ✨ Features

- **URL Downloader**: Enter any YouTube URL to fetch and download audio directly to your library.
- **Integrated Search**: Search for songs by name and preview results via embedded YouTube iframes.
- **Smart Playlists**: Add your favorite tracks to a persistent playlist and play them sequentially.
- **Simplified Auth**: Fast login and registration using only a unique username.
- **Sleek UI**: A modern, responsive interface inspired by top-tier streaming services.

## 🛠️ Tech Stack

### Backend
- **Flask**: The core web framework.
- **SQLite3**: Lightweight, reliable database for user and playlist storage.
- **yt-dlp**: Powerful engine for handling YouTube metadata and downloads.

### Core Dependencies
- `Flask (3.1.3)`: Primary framework.
- `yt-dlp (2026.3.17)`: YouTube integration and downloading.
- `Flask-JWT-Extended (4.7.4)`: Secure, token-based authentication.
- `flask-cors (6.0.2)`: Handling cross-origin requests.

### Sub-packages & Utilities
- `Werkzeug`, `Jinja2`, `itsdangerous`, `MarkupSafe`: Flask internals and templating.
- `PyJWT`: JWT implementation.
- `blinker`, `click`: Signaling and CLI support.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- FFmpeg (required by yt-dlp for audio conversion)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/1anonymous47/yt_song.git
   cd yt_song
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   flask run
   ```
   The app will be available at `http://127.0.0.1:5000`.

## 📂 Project Structure
- `app.py`: Main Flask application and routes.
- `models.py`: SQLite database schemas.
- `downloader.py`: logic for yt-dlp integration.
- `templates/`: HTML screens for search, downloader, and playlist.
- `static/`: CSS and client-side JavaScript.

---
*Created with focus on performance and clean design.*