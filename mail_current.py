import os
import json
import base64
from email import message_from_bytes
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    creds = None
    if os.path.exists('token.json'):
        with open('token.json', 'r') as token:
            creds = Credentials.from_authorized_user_info(json.load(token))

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Get the current date and the start of the next day in RFC3339 format
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
    tomorrow_start = (datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)).isoformat() + 'Z'

    # Use the query parameter to filter messages from today
    query = f'after:{today_start} before:{tomorrow_start}'

    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No messages found.')
    else:
        for msg in messages:
            msg = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            payload = msg.get('payload')
            headers = payload.get('headers')
            subject = ''
            for header in headers:
                if header.get('name') == 'Subject':
                    subject = header.get('value')

            snippet = msg.get('snippet')

            print('Message snippet:', snippet)
            print('Message subject:', subject)

if __name__ == '__main__':
    main()
