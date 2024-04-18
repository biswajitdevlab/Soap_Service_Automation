"""
import requests

class SOAPClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def send_request(self, request_body):
        headers = {'Content-Type': 'text/xml'}
        response = requests.post(self.endpoint, data=request_body, headers=headers)
        return response
"""
# soap_clients.py
import requests

class SOAPClient:
    def __init__(self):
        pass

    def send_request(self, url, method='POST', data=None, params=None):
        headers = {'Content-Type': 'text/xml'}

        if method == 'POST':
            response = requests.post(url, data=data, headers=headers)
        elif method == 'GET':
            response = requests.get(url, params=params, headers=headers)
        else:
            raise ValueError("Invalid HTTP method. Supported methods are 'POST' and 'GET'.")

        return response
