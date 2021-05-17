from setuptools import setup, find_packages

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps'],
    'resources': ['config.ini', 'accounts.json']
}

setup(
    name='Toony',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    packages=find_packages()
)