# cd_drive

cd Drive is a wrapper of google-api-python-client that make it easier to manipulate files on Google Drive.

# Installation

You can install cd_drive using `pip`:

```
pip install cd_drive
```

# Usage

First [enable Google Drive API on your google account](https://developers.google.com/drive/api/v3/enable-drive-api) and download the `credentials.json` file. With the credentials file you can start using cd_drive:

```python
from cd_drive import Drive

# Perform oAuth flow to authorize application
drive = Drive('path/to/credentials.json')

# Select current dir
drive.cd('Images/')

# Read file from Google Drive at the current dir
img = drive.read('photo.png')

# Write file on Google Drive at the current dir
drive.write('new-photo.png')
```

