"""
Meowify API - FastAPI application for audio processing with meowifylib.

This API provides endpoints for processing audio files with the meowifylib package.
"""


import os
import io
import tempfile
from typing import List

import librosa
import soundfile as sf
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import Response
from pydantic import BaseModel

from meowifylib.run import meowify_song

# Configure environment
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

model_checkpoint = "/checkpoint/trained.ckpt"

# Initialize FastAPI app
app = FastAPI(title="Meowify API", description="API for Meowify audio processing")


class SampleInfo(BaseModel):
    pitch: int
    index: int


@app.post("/meowify/", response_class=Response)
async def meowify_audio(
    audio_file: UploadFile = File(...),
    samples: List[UploadFile] = File(...),
    sample_infos: str = Form(...),
):
    """
    Process an audio file to create a meowified version.

    Parameters:
    - audio_file: The input audio file to process
    - samples: List of sample audio files to use for synthesis
    - sample_infos: JSON string containing pitch information for each sample

    Returns:
    - The processed audio file as WAV
    """
    import json

    sample_infos = json.loads(sample_infos)

    # Create temporary directory for processing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save the uploaded audio file
        input_path = os.path.join(temp_dir, "input.wav")
        with open(input_path, "wb") as f:
            f.write(await audio_file.read())

        # Save the sample files
        sample_paths = []
        for i, sample_file in enumerate(samples):
            sample_path = os.path.join(temp_dir, f"sample_{i}.wav")
            with open(sample_path, "wb") as f:
                f.write(await sample_file.read())
            sample_paths.append(sample_path)

        # Create sample choices
        sample_choices = []
        i = 0
        for info in sample_infos:
            sample_choices.append({"name": sample_paths[i], "pitch": info["pitch"]})
            i += 1

        # Use meowify_song function to process the audio
        mixed_audio = meowify_song(input_path.split(".")[0], sample_choices, model_checkpoint)

        # Save the result to a BytesIO object
        output_buffer = io.BytesIO()
        sf.write(output_buffer, mixed_audio, 22050, format="WAV")
        output_buffer.seek(0)

        # Return the audio file
        return Response(content=output_buffer.read(), media_type="audio/wav")


@app.get("/")
async def root():
    return {"message": "Welcome to Meowify API"}
