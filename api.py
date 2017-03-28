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
    ''' Контрольная сумма для данного пути и параметров. '''
    params = urlencode(params)
    return md5(
        md5(SECRET) +
        md5(path) +
        md5(params)
    )


def api_request(api_version, path, params):
    '''
    Синхронный запрос к API. Путь (path) указывается с / в начале.
    Возвращает requests.Response.
    '''
    params = OrderedDict(sorted(params.items()))
    params["checksum"] = checksum(path, params)
    params["key"] = KEY
    url = API_URL + str(api_version) + path
    resp = requests.get(url, params=params)
    return resp


def get_item(id):
    '''
    Получение лота с номером id.
    Возвращает requests.Response.
    '''
    path = "/items/{}"
    return api_request(API_VERSIONS[path], path.format(id), {})
