import json
from requests.auth import HTTPBasicAuth

from django.conf import settings
from core.client import BaseClient
from core.http import HttpClient


class ZenDeskClient(BaseClient):

    def __init__(self, host, username, password):

        self.base_url = self.get_api_baseurl(settings.EXTERNAL_SERVICES["ZENDESK"]["HOST"], secure=True)
        self.request_headers = settings.EXTERNAL_SERVICES["ZENDESK"]["HEADERS"]

    def update_ticket(self, ticket_id, attribute_dict):

        url = self.base_url + '/api/v2/tickets/' + str(ticket_id) + '.json'
        body = {
            "ticket": attribute_dict
        }
        response = HttpClient().put(url, headers=self.request_headers, data=json.dumps(body), auth=HTTPBasicAuth(self.username, self.password))
        return response

    def get_ticket_comments(self, ticket_id, include=[], sort_order="asc"):

        include_str = self.get_include_string(include)
        url = self.base_url + '/api/v2/tickets/' + str(ticket_id) + '/comments?include=' + include_str + '&sort_order=' + sort_order
        response = HttpClient().get(url, headers=self.request_headers, auth=HTTPBasicAuth(self.username, self.password))
        return response
