import os
import yt_dlp


def download_audio(url):
    os.makedirs("downloads", exist_ok=True)

    output_template = "downloads/%(title)s.%(ext)s"

    options = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)

        title = info.get("title", "audio")

        filename = ydl.prepare_filename(info)
        mp3_file = os.path.splitext(filename)[0] + ".mp3"

        return mp3_file, title