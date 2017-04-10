import datetime
from dateutil.parser import parse
import json

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials

CALENDAR_ID = 'bleh@group.calendar.google.com'

def create_event_from_message(message):

    start_datetime = parse(message['pass_begin'])
    end_datetime = parse(message['pass_end'])

    event = {
        'summary': message['satellite']['name'],
        'location': 'Des Moines, IA',
        'description': message['satellite']['frequency'],
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'Etc/UTC'
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'Etc/UTC'
        }
    }

    return event

def post_to_google_calendars(event_body):
    scopes = ['https://www.googleapis.com/auth/calendar']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        './SatStalkerPredictor.json',
        scopes
    )

    http_auth = credentials.authorize(Http())

    service = build('calendar', 'v3', http=http_auth)

    service.events().insert(
        calendarId=CALENDAR_ID,
        body=event_body
    ).execute()

def lambda_handler(event, context):
    for record in event['Records']:
        parsed_record = json.loads(record['Sns']['Message'])

        new_event = create_event_from_message(parsed_record)

        post_to_google_calendars(new_event)

def main():
    lambda_handler(None, None)

if __name__ == '__main__':
    main()
