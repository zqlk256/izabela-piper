#!/usr/bin/env python3

from piper import speak
from voice import Voice, scan_voice_dir
from flask import Flask, request, Response
from flask_cors import CORS

# load settings from config file
from config import Config
config = Config('settings.toml')

# create flask app
app = Flask(__name__)
CORS(app)

# load voices and put them in a dictionary
voices = {voice.id(): voice for voice in scan_voice_dir(config.voice_dir)}


@app.route("/")
def index():
    """Endpoint to show a simple HTML page"""
    return f"<h1>Piper Web Interface</h1><p>This web server provides access to {len(voices)} different voices!</p>"


@app.route('/list-voices', methods=['GET', 'POST'])
def list_voices():
    """Endpoint to list all available voices"""
    # sort voices by path, then by speaker
    def get_sort_key(voice: Voice): return (voice.path, voice.speaker_id)
    items = sorted(voices.items(), key=lambda item: get_sort_key(item[1]))
    return [
        {
            "id": id,
            "name": voice.name,
            "languageCode": voice.language
        } for (id, voice) in items
    ]


@app.route('/synthesize-speech', methods=['POST'])
def synthesize_speech():
    """Endpoint to synthesize speech from text"""
    # parse request data
    data = request.get_json()
    payload = data['payload']
    text = payload['text']
    id = payload['voice']['id']

    # run piper
    wav_data = speak(text, voices[id], config.piper_exe, config.piper_args)
    return Response(wav_data, mimetype='audio/wav')


if __name__ == '__main__':
    # set up logging
    import logging
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.INFO)

    # start server
    from waitress import serve
    serve(app, host=config.host, port=config.port)
