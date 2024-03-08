from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def add_event(event_details, creds):
    service = build("calendar", "v3", credentials=creds)
    event = service.events().insert(calendarId='primary', body=event_details).execute()
    print('Event created: %s' % (event.get('htmlLink')))

    
