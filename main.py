#!/usr/bin/env python3

from piper import speak
from voice import Voice, scan_voice_dir
from flask import Flask, request, Response
from flask_cors import CORS
from dynaconf import Dynaconf

# load settings from config file
settings = Dynaconf(settings_files=['settings.toml'])

# create flask app
app = Flask(__name__)
CORS(app)

# load voices and put them in a dictionary
voices = {voice.id(): voice for voice in scan_voice_dir(settings.voice_dir)}


@app.route("/")
def index():
    return f"<h1>Piper Web Interface</h1><p>This web server provides access to {len(voices)} different voices!</p>"


@app.route('/list-voices', methods=['GET', 'POST'])
def list_voices():
    """Endpoint to list all available voices"""
    # sort voices by path, then by speaker
    def get_sort_key(voice: Voice): return (voice.path, voice.speaker_id)
    return [
        {
            "id": voice.id(),
            "name": voice.name,
            "languageCode": voice.language
        } for voice in sorted(voices.values(), key=get_sort_key)
    ]


@app.route('/synthesize-speech', methods=['POST'])
def synthesize_speech():
    """Endpoint to synthesize speech from text"""
    # parse request data
    data = request.get_json()
    payload = data['payload']
    text = payload['text']
    id = payload['voice']['id']

    # get piper stuff from settings
    piper_exe: str = settings.piper_exe  # type: ignore
    piper_args: list[str] = settings.piper_args  # type: ignore

    wav_data = speak(text, voices[id], piper_exe, piper_args)
    return Response(wav_data, mimetype='audio/wav')


if __name__ == '__main__':
    # set up logging
    import logging
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.INFO)

    # start server
    from waitress import serve
    serve(app, host=settings.host, port=settings.port)
