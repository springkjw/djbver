import time
import base64
import hmac
import hashlib
import requests
from enum import Enum
from django.conf import settings
from django.utils import timezone

from .base import BaseSMS


__all__ = ['NCloud']


class Status(Enum):
    ACCEPT = "202"
    BAD_REQUEST = "400"
    UNAUTHORIZED = "401"
    FORBIDDEN = "403"
    NOT_FOUND = "404"
    TOO_MANY_REQUESTS = "429"
    INTERNAL_SERVER_ERROR = "500"


class Name(Enum):
    SUCCESS = "success"
    RESERVED = "reserved"
    SCHEDULED = "scheduled"
    FAIL = "fail"


class NCloudSMS(BaseSMS):
    HOST = 'https://sens.apigw.ntruss.com'

    def make_timestamp(self):
        timestamp = int(time.time() * 1000)
        return str(timestamp)

    def make_signature(self, uri, method):
        access_key = settings.NCP_ACCESS_KEY
        secret_key = settings.NCP_SECRET_KEY
        secret_key = bytes(secret_key, 'UTF-8')

        message = "{method} {uri}\n{timestamp}\n{access_key}".format(
            method=method,
            uri=uri,
            timestamp=self.make_timestamp(),
            access_key=access_key
        )
        message = bytes(message, 'utf-8')
        signing_key = base64.b64encode(
            hmac.new(
                secret_key,
                msg=message,
                digestmod=hashlib.sha256
            ).digest()
        ).decode()
        return signing_key

    def make_header(self, uri, method) -> dict:
        return {
            'content-type': 'application/json; charset=utf-8',
            'x-ncp-apigw-timestamp': self.make_timestamp(),
            'x-ncp-iam-access-key': settings.NCP_ACCESS_KEY,
            'x-ncp-apigw-signature-v2' : self.make_signature(uri, method)
        }

    def send_sms(self, phone, body):
        uri = '/sms/v2/services/{service_id}/messages'.format(
            service_id=settings.NCP_SERVICE_ID
        )
        url = "{host}{uri}".format(host=self.HOST, uri=uri)

        data = {
            "type": "SMS",
            "from": settings.SEND_PHONE,
            "content": body,
            "messages": [{"to": self.clean_number(phone)}]
        }

        res = requests.post(
            url,
            data=data,
            headers=self.make_header(uri=uri, method="POST")
        )
        result = res.json()

        status_code = result.get('statusCode')
        status_name = result.get('statusName')
        request_id = result.get('requestId')

        if Status(status_code) == Status.ACCEPT and Name(status_name) == Name.SUCCESS:
            return True, status_code, request_id
        return False, status_code, None

    def retreive_sms(self, request_id):
        uri = '/sms/v2/services/{service_id}/messages?requestId={request_id}'.format(
            service_id=settings.NCP_SERVICE_ID,
            request_id=request_id
        )
        url = "{host}{uri}".format(host=self.HOST, uri=uri)

        res = requests.get(
            url,
            headers=self.make_header(uri=uri, method="GET")
        )
        result = res.json()