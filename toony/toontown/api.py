import hashlib
import json
import time
import urllib.parse
import urllib.request
from http.client import HTTPResponse
from typing import Optional


__LOGIN_ENDPOINT = 'https://www.toontownrewritten.com/api/login'
__POPULATION_ENDPOINT = 'https://www.toontownrewritten.com/api/population'
__HEADERS = {'Content-type': 'application/x-www-form-urlencoded',
             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                           'Version/14.0.2 Safari/605.1.15'}


class ConnectionException(Exception):
    """This is raised when the Toontown Rewritten servers cannot be reached"""


class FailedLoginException(Exception):
    """This is raised when the launcher has failed to login the user"""


class FailedAuthException(Exception):
    """This is raised when the launcher has failed to authenticate the user"""


def login(username: str, password: str):
    gameserver, playcookie = __connect_to_server(username, password)
    return gameserver, playcookie


def get_population() -> str:
    population_data = request(None, __POPULATION_ENDPOINT, format='json')
    return str(population_data['totalPopulation'])


def __connect_to_server(username: str, password: str):
    http_request_params = {'username': username, 'password': password}
    http_response = request(http_request_params, __LOGIN_ENDPOINT)

    if http_response['success'] == 'false':  # username or password is incorrect
        raise FailedLoginException(http_response['banner'])
    elif http_response['success'] == 'partial':  # user needs to authenticate with toonguard
        while http_response['success'] == 'partial':
            return

    if http_response['success'] == 'delayed':  # user is queued to enter the game
        http_request_params = {'queueToken': http_response['queueToken']}
        while http_response['success'] == 'delayed':
            time.sleep(1)
            http_response = request(http_request_params, __LOGIN_ENDPOINT)

    if http_response['success'] != 'true':  # make sure user is logged in
        raise FailedLoginException(http_response.get('banner', 'Failed to login.'))

    return http_response['gameserver'], http_response['cookie']


def request(params: Optional[dict], endpoint: str, format: Optional[str] = None):
    if params:
        data = urllib.parse.urlencode(params).encode()
    else:
        data = None

    req = urllib.request.Request(endpoint, headers=__HEADERS, data=data)

    with urllib.request.urlopen(req) as resp:
        if resp.status != 200:
            raise ConnectionException(f'Failed to reach login server with status code: {resp.status}')

        if format == 'json':
            data = json.loads(resp.read().decode('utf-8'))
        else:
            data = __parse_httpresponse(resp)
        return data


def __parse_httpresponse(resp: HTTPResponse):
    data = resp.read().decode('utf-8').strip().split('\n')
    data = dict(((t.split('=')[0], t.split('=')[1]) for t in data))
    return data
