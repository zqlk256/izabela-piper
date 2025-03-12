import os
import sys
from dynaconf import Dynaconf


def resource_path(relative_path):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
    else:
        exe_dir = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(exe_dir, relative_path)


settings = Dynaconf(
    settings_files=[resource_path('settings.toml')],
)
