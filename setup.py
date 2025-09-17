# setup.py (py2app)
from setuptools import setup

APP = ['main.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PIL', 'qrcode', 'mysql', 'mysql.connector'],
    # iconfile: opcional, si tienes assets/miqr.icns
    'iconfile': 'assets/miqr.icns'  
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
