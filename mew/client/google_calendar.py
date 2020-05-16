import logging

from django.conf import settings
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/calendar']


class GoogleCalendarClient():

    def __init__(self, extra_headers=None):
        service_conf = settings.EXTERNAL_SERVICES.get("GOOGLE", {}).get("CALENDAR", {})
        self.credentials = service_account.Credentials.from_service_account_info(service_conf.get("CREDENTIALS", {}), scopes=SCOPES)

    def __prepare_new_event_body(self, event_data):
        """
        """
        event_body = {
            'summary': event_data.get("summary"),
            'location': '',
            'description': event_data.get("description"),
            'start': {
                'dateTime': event_data.get("start_time"),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': event_data.get("end_time"),
                'timeZone': 'UTC',
            },
            'conferenceDataVersion': 1,
            'recurrence': event_data.get("recurrence", []),
            'attendees': event_data.get("attendees"),
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': event_data.get("reminder_time", 30 * 60)},
                ],
            },
        }
        return event_body

    def __prepare_update_event_body(self, event_data):
        """
        """
        event_body = {}
        if event_data.get("start_time"):
            event_body['start'] = {
                'dateTime': event_data.get("start_time"),
                'timeZone': 'UTC',
            }
        if event_data.get("end_time"):
            event_body['end'] = {
                'dateTime': event_data.get("end_time"),
                'timeZone': 'UTC',
            }
        if event_data.get("attendees"):
            event_body["attendees"] = event_data.get("attendees")

        return event_body

    def create_event(self, calendar_data):
        """
        """
        delegated_credentials = self.credentials.with_subject(calendar_data.get("organizer"))
        service = build('calendar', 'v3', credentials=delegated_credentials)

        # Call the Calendar API
        body = self.__prepare_new_event_body(calendar_data)

        logging.info("Calling Google Calendar Event Creation API with data -- %s" % (body))
        event = service.events().insert(calendarId='primary', body=body).execute()
        logging.info("Calendar API Event Creation Response -- %s" % (event))
        return event

    def get_event_details(self, calendar_email, event_id):
        """
        """
        delegated_credentials = self.credentials.with_subject(calendar_email)
        service = build('calendar', 'v3', credentials=delegated_credentials)
        logging.info("Calling Google Event GET API -- %s, %s" % (event_id, calendar_email))
        event = service.events().get(calendarId='primary', eventId=event_id).execute()
        logging.info("Google Calendar Event GET API Response -- %s" % (event))
        return event

    def update_event(self, event_id, event_data):
        """
        """
        delegated_credentials = self.credentials.with_subject(event_data.get("organizer"))
        service = build('calendar', 'v3', credentials=delegated_credentials)
        logging.info("Calling Google Event PUT API -- %s" % (event_data))

        logging.info("Calling Google Event GET API -- %s" % (event_id))
        event = service.events().get(calendarId='primary', eventId=event_id).execute()
        logging.info("Google Calendar Event GET API Response -- %s" % (event))
        if not event:
            logging.info("Something went wrong. The event might not exist.")
            return False

        event_body = self.__prepare_update_event_body(event_data)
        logging.info("Calling Google Event PUT API -- %s" % (event_body))
        event.update(event_body)
        updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
        logging.info("Google Event PUT API Response -- %s" % (updated_event))
        return updated_event
