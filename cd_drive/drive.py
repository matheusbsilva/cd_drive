import pickle
import os.path
import io

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload, MediaIoBaseUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class Drive:
    """
    Class for manipulating files on Google Drive.
    """

    def __init__(self, credentials_file, token_file='./.token.pickle'):
        self.creds = None
        self.service = None
        self.client_secrets_file = credentials_file
        self.token_file = token_file
        self.scopes = ['https://www.googleapis.com/auth/drive']
        self.current_dir_id = None

        self.service = self.auth()

    def auth(self):
        """
        Perform oAuth flow and store temporary token on a pickle file
        """

        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                        self.client_secrets_file, self.scopes)

                self.creds = flow.run_local_server(port=0)

            with open(self.token_file, 'wb') as token:
                pickle.dump(self.creds, token)

        service = build('drive', 'v3', credentials=self.creds)

        return service

    def cd(self, path):
        current_dir_id = None

        if path.endswith('/'):
            path = path[:-1]

        folders = [path]
        if '/' in path:
            folders = path.split('/')

        for folder in folders:
            files = None

            if current_dir_id:
                query = "'{}' in parents".format(current_dir_id)
                results = self.search(query)

                for result in results:
                    if result['name'] == folder:
                        files = [result]

            else:
                query = "name = '{}'".format(folder)
                files = self.search(query)

            if not files:
                # TODO: Create Exception class
                raise BaseException("Directory not found: {}".format(folder))

            current_dir_id = files[0].get('id', None)

        self.current_dir_id = current_dir_id

        return self.current_dir_id

    def search(self, query, fields="files(id, name)"):
        results = self.service.files().list(fields=fields, q=query).execute()
        files = results.get('files', [])

        return files

    def read(self, file, write_dir='/tmp/'):
        if write_dir[-1] != '/':
            write_dir = "{}/".format(write_dir)

        if self.current_dir_id:
            query = "name='{}' and '{}' in parents".format(file,
                                                           self.current_dir_id)
        else:
            query = "name='{}'".format(file)

        result = self.search(query)

        if not result:
            raise BaseException("File not found: {}".format(file))

        file_id = result[0]['id']

        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO('{}{}'.format(write_dir, file), mode='w+')

        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download {}%.".format(int(status.progress() * 100)))

        return fh

    def write(self, filename, mimetype, filepath=None, buff=None):
        file_metadata = {'name': filename, "parents": [self.current_dir_id]}

        if buff:
            media = MediaIoBaseUpload(buff, mimetype=mimetype, resumable=True)
        else:
            if not filepath:
                raise ValueError('Provide a valid value for `filepath` or `buff`')
            media = MediaFileUpload(filepath, mimetype=mimetype)

        file = self.service.files().create(
                body=file_metadata, media_body=media, fields='id').execute()

        return file.get('id')

