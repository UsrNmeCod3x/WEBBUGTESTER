import requests

class HTTPClient:
    def __init__(self, proxy=None):
        self.session = requests.Session()
        self.session.verify = False
        if proxy:
            self.session.proxies = {"http": proxy, "https": proxy}

    def get(self, url, **kwargs):
        return self.session.get(url, timeout=15, **kwargs)
