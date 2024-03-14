from rest_framework import status
from rest_framework.exceptions import APIException


class CustomBaseException(APIException):
    detail = None
    status_code = None

    def __init__(self, detail, code):
        super().__init__(detail, code)
        self.detail = detail
        self.status_code = code


class InvalidRequestException(CustomBaseException):
    def __init__(self, detail='Bad request.'):
        super().__init__(detail, status.HTTP_400_BAD_REQUEST)
