import traceback
import threading
import uuid

from django.http import JsonResponse
from django.conf import settings

from requests.exceptions import HTTPError


class DefaultHandler(object):

    request_id = {}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.set_request_id()
        response = self.get_response(request)
        self.delete_request_id()
        return response

    def is_registered(self, exception):
        try:
            return exception.is_an_error_response
        except AttributeError:
            return False

    def process_exception(self, request, exception):

        status = None
        exception_dict = {}

        if self.is_registered(exception):
            status = exception.status_code
            exception_dict = exception.to_dict()

        elif isinstance(exception, HTTPError):
            if hasattr(exception, 'response'):
                error_info = {
                    'message': exception.response._content.decode('utf-8'),
                    'url': exception.response.url,
                    'status_code': exception.response.status_code
                }
                status = exception.response.status_code
                exception_dict = {'error': 'Something Went Wrong.', 'response': '', 'error_info': error_info}

        if not status:
            status = 500
            exception_dict = {'error': 'Some Unexpected Error Occurred.', 'response': ''}

        if settings.CONFIG and settings.CONFIG.get("SENTRY", {}) and settings.CONFIG.get("SENTRY", {}).get("ENABLED", False):
            SentryExceptionHandler().capture(exception)

        traceback.print_exc()
        return JsonResponse(exception_dict, status=status)

    @classmethod
    def set_request_id(self):
        self.request_id[threading.current_thread()] = str(uuid.uuid4())

    @classmethod
    def get_request_id(self):
        return self.request_id.get(threading.current_thread(), "No-Request-ID")

    @classmethod
    def delete_request_id(self):
        request_id = self.get_request_id()
        if request_id:
            self.request_id.pop(threading.current_thread(), None)


class SentryExceptionHandler(object):

    def capture(self, exception):
        from sentry_sdk import capture_exception
        capture_exception(exception)
