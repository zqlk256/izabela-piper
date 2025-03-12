import os
import sys
from typing import List
from pathlib import Path


def _resource_path(relative_path):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
    else:
        exe_dir = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(exe_dir, relative_path)


def _args_to_list(args) -> List[str]:
    """Converts a config value to an argument list."""
    if isinstance(args, str):
        return args.split()
    else:
        return [str(arg) for arg in args]


class Config:
    def __init__(self, path: str):
        from dynaconf import Dynaconf
        conf = Dynaconf(settings_files=[_resource_path(path)])

        self.host: str = conf.host  # type: ignore
        self.port: int = conf.port  # type: ignore
        self.voice_dir = Path(conf.voice_dir)  # type: ignore
        self.piper_exe = Path(conf.piper_exe)  # type: ignore
        self.piper_args = _args_to_list(conf.piper_args)
