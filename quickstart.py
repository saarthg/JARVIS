import datetime
from datetime import date
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from gcalendar import add_event
from generate_json import generate_json
from gmail import gmail_create_draft

import streamlit as st
from audiorecorder import audiorecorder

from speech_to_text import speech_to_text


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/gmail.compose"]


def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    now = date.today()

    st.title("Gmail/Google Calendar Automation")
    audio = audiorecorder("Click to record", "Click to stop recording")

    if len(audio) > 0:
       audio.export("audio.wav", format="wav")
       
       query = speech_to_text()
       os.remove("audio.wav")
       json_response, function_called = generate_json(query + f"The date today is {now}")
       if function_called == "add_event":
          add_event(json_response, creds)
          st.write("Event has been added to your calendar.")
       elif function_called == "add_draft":
          print(json_response)
          gmail_create_draft(json_response["content"], json_response["to"], "saarthgao@gmail.com", json_response["subject"], creds)
          st.write("Email draft has been created.")


    query = st.text_input("Enter your query.")

    if query:
        json_response, function_called = generate_json(query + f"The date today is {now}")
        if function_called == "add_event":
            add_event(json_response, creds)
            st.write("Event has been added to your calendar.")
        elif function_called == "add_draft":
            print(json_response)
            gmail_create_draft(json_response["content"], json_response["to"], "saarthgao@gmail.com", json_response["subject"], creds)
            st.write("Email draft has been created.")

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()