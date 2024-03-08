import json
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
from datetime import date


load_dotenv(".env")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_KEY

def generate_json(query):
    client = OpenAI()
    functions = [
  {
    "name": "add_event",
    "description": "Get the event information from the input text.",
    "parameters": {
      "type": "object",
      "properties": {
        "summary": {
          "type": "string",
          "description": "Title of the event"
        },
        "location": {
          "type": "string",
          "description": "Location of the event"
        },
        "description": {
          "type": "string",
          "description": "Description about the event"
        },
        "start": {
          "type": "object",
          "properties": {
            "dateTime": {
              "type": "string",
              "description": "Start time in the following format: 2024-05-28T09:00:00-07:00."
            },
            "timeZone": {
              "type": "string",
              "description": "Time zone of the event, default is America/Los_Angeles"
            }
          }
        },
        "end": {
          "type": "object",
          "properties": {
            "dateTime": {
              "type": "string",
              "description": "End time in the following format: 2024-05-28T09:00:00-07:00"
            },
            "timeZone": {
              "type": "string",
              "description": "Time zone of the event, default is America/Los_Angeles"
            }
          }
        },
        "attendees": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "email": {
                "type": "string",
                "description": "Email address of the attendee"
              }
            }
          },
          "description": "List of attendees for the event"
        }
      }
    }
  },
  {
    "name": "add_draft",
    "description": "Get the email content, to and from email addresses, and subject from the input text.",
    "parameters": {
      "type": "object",
      "properties": {
        "content": {
          "type": "string",
          "description": "Content of the email message"
        },
        "to": {
          "type": "string",
          "description": "email address that message is being sent to"
        },
        "from": {
          "type": "string",
          "description": "email address of sender, default is saarthgao@gmail.com"
        },
        "subject": {
          "type": "string",
          "description": "Subject of the email"
        }
      }
    }
  }
]
    
    response = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [{'role': 'user', 'content': query}],
        functions = functions,
        function_call = 'auto'
    )

    json_response = json.loads(response.choices[0].message.function_call.arguments)

    response_message = response.choices[0].message
    function_called = None

    #function_args  = json.loads(response_message.function_call.arguments)

    if dict(response_message).get('function_call'):
        function_called = response_message.function_call.name

    return json_response, function_called