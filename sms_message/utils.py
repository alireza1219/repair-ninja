"""
Inspired from https://github.com/IPeCompany/SmsPanelV2.Python.
"""
from typing import List
from django.conf import settings
from requests.models import Response
from requests.exceptions import ConnectTimeout, HTTPError, ReadTimeout, Timeout

import requests


LINE_NUMBER = settings.SMS_LINE_NUMBER or None
API_KEY = settings.SMS_API_KEY


class SmsMessage():
    """
    This class is responsible for sending sms messages to a phone number.

    The full API documentation for SMS.ir can be found here:
    https://sms.ir/developer-web-service/rest-api/
    """
    API_ENDPOINT = 'https://api.sms.ir'

    def __init__(self, api_key: str = API_KEY, linenumber: int = LINE_NUMBER) -> None:
        self._linenumber = linenumber
        self._headers = {
            'X-API-KEY': api_key,
            'ACCEPT': 'application/json',
            'Content-Type': 'application/json',
        }

    def send_sms(self, number: str, message: str, linenumber: int = None) -> Response:
        """
        Sends a message to a specific phone number.
        """
        return self.send_bulk_sms(
            numbers=[number],
            message=message,
            linenumber=linenumber
        )

    def send_bulk_sms(self, numbers: List[str], message: str, linenumber: int = None) -> Response:
        """
        Sends a message to multiple phone numbers.
        """
        url = f"{self.API_ENDPOINT}/v1/send/bulk/"

        data = {
            'lineNumber': linenumber or self._linenumber,
            'MessageText': message,
            'Mobiles': numbers,
        }

        return self.post(url, data)

    def post(self, url, data):
        """
        Sends a post request to a url with the given data.
        """
        try:
            return requests.post(url, headers=self._headers, json=data, timeout=15)
        except (ConnectionError, ConnectTimeout, HTTPError, ReadTimeout, Timeout) as e:
            # TODO: Logging.
            return self.fake_response(e.request)

    def fake_response(self, request):
        """
        Generates a fake response object with a status code of 503.
        """
        response = requests.models.Response()
        response.status_code = 503
        response.request = request
        response.url = request.url

        return response
