import hashlib
from collections import OrderedDict
from urllib.parse import urlencode

import requests

from config import API_URL, SECRET, KEY

API_VERSIONS = {
    "/items/{}": 7
}


def md5(string):
    return hashlib.md5(string.encode("utf8")).hexdigest()


def checksum(path, params):
    ''' Checksum for given path and params. '''
    params = urlencode(params)
    return md5(
        md5(SECRET) +
        md5(path) +
        md5(params)
    )


def api_request(api_version, path, params):
    '''
    Synchronous API request. Path should start with /.
    Returns requests.Response.
    '''
    params = OrderedDict(sorted(params.items()))
    params["checksum"] = checksum(path, params)
    params["key"] = KEY
    url = API_URL + str(api_version) + path
    resp = requests.get(url, params=params)
    return resp


def get_item(id):
    '''
    Getting lot with given id.
    Returns requests.Response.
    '''
    path = "/items/{}"
    return api_request(API_VERSIONS[path], path.format(id), {})
