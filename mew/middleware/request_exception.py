import traceback
from django.http import JsonResponse
from django.conf import settings

from requests.exceptions import HTTPError


class RequestExceptionHandler(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

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


class SentryExceptionHandler(object):

    def capture(self, exception):
        from sentry_sdk import capture_exception
        capture_exception(exception)
