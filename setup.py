from setuptools import setup

APP = ['modifiles.py']  # Main Python script
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': [],  # Any additional packages used
    'plist': {
        'CFBundleName': 'Modifiles',
        'CFBundleShortVersionString': '0.1',
        'CFBundleVersion': '0.1',
        'CFBundleIdentifier': 'com.gmail.bokyere887.Modifiles',
        'Entitlements': 'Entitlements.plist', 
    },
    'bundle_files': 1,   # Create a single executable app
    'includes': [],  # Specify any additional modules if necessary
    'excludes': [],  # Exclude unnecessary modules
}

setup(
    app=APP,
    name='Modifiles',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
