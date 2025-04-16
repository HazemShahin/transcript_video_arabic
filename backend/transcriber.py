import whisper
import os
from audio_downloader import download_audio

#download_audio("https://www.youtube.com/watch?v=FQBdpPrLj9k&list=PLnFJTGgdQYTNJLSn8ENSzD9qaPz3LypyW&index=5", "Almuahdara5")
model = whisper.load_model("large", device="cpu")

def transcribe_audio(audio_path: str, language: str = "arabic") -> str:
    result = model.transcribe(audio_path, language="ar",task = "transcribe")
    return result["text"]

def save_transcript_as_txt(text: str, audio_path: str, model_name: str):
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    txt_path = os.path.join("downloads", f"{base_name}_{model_name}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Transcript saved to: {txt_path}")
    return txt_path

# Usage
if __name__ == "__main__":
    path = os.path.join("downloads", "Almuahdara5.mp3")
    text = transcribe_audio(path, "ar")
    save_transcript_as_txt(text, path, "large")
