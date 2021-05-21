from setuptools import setup, find_packages

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',
    'plist': {
        'LSUIElement': True,
        'CFBundleIdentifier': 'thewallacems.Toony',
        'CFBundleVersion': '2021.05.17',
        'CFBundleShortVersionString': '2021.05.17',
        'NSHumanReadableCopyright': 'thewallacems',
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
