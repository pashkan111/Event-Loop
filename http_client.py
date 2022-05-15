from yarl import URL
from async_socket import AsyncSocket
import json


class HttpClientAbstract:
    def get():
        raise NotImplementedError

    def post():
        raise NotImplementedError


class Client(HttpClientAbstract):
    request_string = '{method} {path} HTTP/1.1\r\n{headers}\r\n\r\n'
    
    def __init__(self):
        self._sock = AsyncSocket()
    
    def get_parsed_url(self, url: str, params: dict)-> URL:
        """
        Returns url that has properties:
        url.host,
        url.port, 
        url.path_qs
        """
        parsed_url = URL(url)
        url = parsed_url.with_query(params)
        return url
    
    def get_headers_string(self, headers: dict, host: str):
        """
        Takes in a dict of headers and returns string of them
        """
        headers = headers.copy()
        headers['Host'] = host
        headers['Connection'] = 'close'
        headers_string = '\r\n'.join(
            f'{key}: {value}'
            for key, value in headers.items()
        )
        return headers_string

    def get_request_string(self, method: str, headers:dict, parsed_url:URL):
        headers_string = self.get_headers_string(headers, parsed_url.host)
        request_string = self.request_string.format(
            method=method,
            path=parsed_url.path_qs, 
            headers=headers_string
            )
        return request_string

    def get(self, url:str, params:dict=None, headers:dict={}):        
        parsed_url = self.get_parsed_url(url, params)
        yield from self._sock.connect(parsed_url.host, parsed_url.port)
        request_string = self.get_request_string(
            'GET', headers, parsed_url
            )
        yield from self._sock.send(request_string)
        data=yield from self._sock.read_all()
        data_decoded = data.decode('utf-8')
        return data_decoded
    
    def post(self, url:str, params:dict, data:dict):
        pass
