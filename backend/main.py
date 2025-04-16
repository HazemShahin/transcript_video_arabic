from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from backend.audio_downloader import download_audio
from backend.transcriber import transcribe_audio
from backend.file_generator import save_transcript_txt, save_transcript_pdf
import uuid
import os

app = FastAPI()

class TranscriptRequest(BaseModel):
    url: str
    language: str = "arabic"  # or "english"

@app.post("/transcribe/")
async def transcribe_endpoint(request: TranscriptRequest, background_tasks: BackgroundTasks):
    try:
        filename = f"{uuid.uuid4()}.mp3"
        audio_path = download_audio(request.url, filename)
        transcript = transcribe_audio(audio_path, request.language)

        txt_file = save_transcript_txt(transcript)
        pdf_file = save_transcript_pdf(transcript)

        return {
            "transcript": transcript,
            "txt_file": txt_file,
            "pdf_file": pdf_file
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))