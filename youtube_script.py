import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http
import time
import random
from persistencia import addYoutube

# Apart from adding the secrets to the 

CLIENT_SECRETS_FILE = "client_secret_3mos.json"

SCOPES = ['https://www.googleapis.com/auth/youtube.upload'] 
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server()
    return googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def initialize_upload(youtube, file, url):
    body = dict(
        snippet = dict(
            title = "Test Video",
            description = "Test Description",
            tags = ["test", "video"],
            categoryId = "22"
        ),
        status = dict(
            privacyStatus = "unlisted",
            selfDeclaredMadeForKids = False
        )
    )

    insert_request = youtube.videos().insert(
        part = ",".join(body.keys()),
        body = body,
        media_body = googleapiclient.http.MediaFileUpload(file, chunksize = -1, resumable = True)
    )

    resumable_upload(insert_request, url)

def resumable_upload(request, url):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print('Uploading file...')
            status, response = request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print(f'Video id "{response["id"]}" was successfully uploaded.')
                    addYoutube(response["id"], url)
                    return response
                else:
                    exit(f'The upload failed with an unexpected response: {response}')
        except googleapiclient.errors.HttpError as e:
            if e.resp.status in [500, 502, 503, 504]:
                error = 'A retriable HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
            else:
                raise
        except Exception as e:
            error = 'An error occurred: %s' % e
        if error is not None:
            print(error)
            retry += 1
            if retry > 10:
                exit('No longer attempting to retry.')
            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print(f'Sleeping {sleep_seconds} seconds and then retrying...')
            time.sleep(sleep_seconds)

# if __name__ == '__main__':
#     youtube = get_authenticated_service()
#     try:
#         initialize_upload(youtube, 'screenrecord2.mp4')
#     except Exception as e:
#         print(f'An error occurred: {e}')