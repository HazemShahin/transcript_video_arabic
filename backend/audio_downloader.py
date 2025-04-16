import yt_dlp
import os

def download_audio(url: str, filename: str) -> str:
    output_path = f"./downloads/{filename}"
    if not os.path.exists("./downloads"):
        os.makedirs("./downloads")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path
# download_audio("https://www.youtube.com/watch?v=FQBdpPrLj9k&list=PLnFJTGgdQYTNJLSn8ENSzD9qaPz3LypyW&index=5", "Aymanlec")
# if __name__ == "__main__":
#     # Example usage
#     download_audio("https://www.youtube.com/watch?v=FQBdpPrLj9k&list=PLnFJTGgdQYTNJLSn8ENSzD9qaPz3LypyW&index=5", "Aymanlec")