from pathlib import Path
from subprocess import run
from typing import List
from voice import Voice

import os
import tempfile
import uuid


def speak(text: str, voice: Voice, piper_exe: Path, piper_args: List[str]) -> bytes:
    """Invokes piper.exe with the given voice and text and returns the resulting WAV data."""

    # Create a unique temporary file name
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, f"piper_{uuid.uuid4().hex}.wav")

    # the bytes to send to piper
    input_bytes = text.encode('utf-8')

    # the piper command line
    command = [
        piper_exe,
        "-q",  # quiet
        "-m", voice.path,
        "-s", str(voice.speaker_id),
        "-f", temp_file,
        *piper_args
    ]

    try:
        # Run the command
        run(command, input=input_bytes, check=True)

        # Read the file
        with open(temp_file, "rb") as f:
            return f.read()

    finally:
        # clean up the temporary file, ignore failure
        try:
            os.remove(temp_file)
        except:
            pass
