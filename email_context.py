import os
import json
import base64
from email import message_from_bytes
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

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

    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=10).execute()
    messages = results.get('messages', [])

    for msg in messages:
        msg = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = msg.get('payload')
        headers = payload.get('headers')
        
        subject = ''
        sender = ''
        for header in headers:
            if header.get('name') == 'Subject':
                subject = header.get('value')
            if header.get('name') == 'From':
                sender = header.get('value')
        
        snippet = msg.get('snippet')
        
        body = ''
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                elif part['mimeType'] == 'text/html':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        else:
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')

        soup = BeautifulSoup(body, 'html.parser')
        p_tags = soup.find_all('p')

        print('Message subject:', subject)
        print('Message snippet:', snippet)
        print('Message sender:', sender)
        print('Message body:')
        for p in p_tags:
            print(p.text)
        print('\n' + '-'*50 + '\n')

if __name__ == '__main__':
    main()
