from setuptools import setup

APP = ['modifiles.py']  # main Python script
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': [],  # Add any additional packages your app uses
    'plist': {
        'CFBundleName': 'Modifiles',
        'CFBundleShortVersionString': '0.1',
        'CFBundleVersion': '0.1',
        'CFBundleIdentifier': 'com.gmail.bokyere887.Modifiles',
        'Entitlements': 'Entitlements.plist', 
    },
}

setup(
    app=APP,
    name='Modifiles',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
