import requests
import urlparse
import xml.etree.ElementTree

class InvalidDataError(LookupError):
    pass

class EVEAPI(object):
    api_server = "https://api.eveonline.com"

    @classmethod
    def api_call(cls, method, api_key):
        url = urlparse.urljoin(cls.api_server, method + ".xml.aspx")
        params = {"keyID": api_key.key_id, "vCode": api_key.vcode, "characterID": api_key.character_id}

        req = requests.post(url, params=params)
        req.raise_for_status()

        root = xml.etree.ElementTree.fromstring(req.text)
        if root is None or root.find("result") is None:
            raise InvalidDataError()

        return root.find("result").find("rowset").findall("row")

