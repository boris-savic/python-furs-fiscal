import json
import jwt

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from requests.exceptions import Timeout
from requests import codes

from furs_fiscal.connector import Connector
from furs_fiscal.exceptions import ConnectionException, ConnectionTimedOutException, FURSException


class FURSBaseAPI(object):
    def __init__(self, p12_path, p12_password, p12_buffer=None, production=True, request_timeout=2.0, proxy=None):
        self.connector = Connector(p12_path=p12_path,
                                   p12_password=p12_password,
                                   p12_buffer=p12_buffer,
                                   production=production,
                                   request_timeout=request_timeout,
                                   proxy=proxy)

    def is_server_accessible(self):
        """
        Check if FURS server is accessible. Will return False if server responds with anything else
        than HTTP Code: 200 or if the request timeouts.

        :return: (boolean) True for ok, False if there was a problem accessing server.
        """
        try:
            return self.connector.send_echo().status_code == codes.ok
        except Timeout as e:
            return False

    def _send_request(self, path, data):
        """
        Sends request to the FURS Server and decodes response.

        :param path: (string) Server path
        :param data: (dict) Data to be sent
        :return: (dict) Received response

        :raises:
            ConnectionTimedOutException: If connection timed out
            ConnectionException: If FURS responded with status code different than 200
            FURSException: If server responded with error
        """
        try:
            response = self.connector.post(path=path, json=data)

            if response.status_code == codes.ok:
                # TODO - we should verify server signature!
                server_response = jwt.decode(response.json()['token'], options={"verify_signature": False})
                return self._check_for_errors(server_response)
            else:
                raise ConnectionException(code=response.status_code,
                                          message=response.text)

        except Timeout as e:
            raise ConnectionTimedOutException(e)

    def _check_for_errors(self, server_response):
        """
        Check if server response contains FURS Error message and raise FURSException if it does
        :param server_response: (dict) FURS Server response data
        :return: server_response: (dict) FURS Server response data

        :raises
            FURSException: If response contains error
        """
        if server_response[list(server_response.keys())[0]].get('Error', None):
            raise FURSException(code=server_response[list(server_response.keys())[0]]['Error']['ErrorCode'],
                                message=server_response[list(server_response.keys())[0]]['Error']['ErrorMessage'])

        return server_response

    def _sign(self, content, algorithm=hashes.SHA256()):
        return self.connector.p12.key.sign(data=bytes(content, 'utf-8'),
                                           padding=padding.PSS(
                                                mgf=padding.MGF1(hashes.SHA256()),
                                                salt_length=padding.PSS.MAX_LENGTH
                                            ),
                                           algorithm=algorithm)
