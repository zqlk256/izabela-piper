import os
import json
import hashlib
from pathlib import Path


class Voice:
    def __init__(self, name: str, path: Path, language: str, speaker_id: int):
        self.name = name
        self.path = path
        self.language = language
        self.speaker_id = speaker_id

    def id(self) -> str:
        """Generates a unique ID for this voice."""
        # the id can be anything, but we need it to be stable across runs
        # so hash() is out. we can use sha256 instead.
        m = hashlib.sha256()
        m.update(bytes(self.path))
        m.update(self.speaker_id.to_bytes())
        return m.hexdigest()


def scan_voice_dir(directory) -> list[Voice]:
    """
    Recursively search for files ending with .onnx in the given directory
    and its subdirectories.
    """
    voices: list[Voice] = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.onnx'):
                # Get the full paths
                onnx_path = Path(root) / file
                json_path = f'{onnx_path}.json'

                try:
                    with open(json_path, 'r', encoding='utf8') as f:
                        json_content = json.load(f)

                    name = onnx_path.stem
                    language = json_content['language']['code']
                    num_speakers = json_content['num_speakers']

                    if num_speakers > 1:
                        voices.extend(
                            Voice(f'{name} (speaker {n})',
                                  onnx_path, language, n)
                            for n in range(num_speakers)
                        )
                    else:
                        # single speaker
                        voices.append(Voice(name, onnx_path, language, 0))

                    print(f"Found {onnx_path}")
                except FileNotFoundError:
                    print(f"Warning: File not found: {json_path}")
                except json.JSONDecodeError:
                    print(f"Warning: Failed to parse file: {json_path}")
                except Exception as e:
                    print(f"Warning: Error reading file {json_path}: {str(e)}")

    print(f'{len(voices)} voices found.')
    return voices
