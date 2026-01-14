import requests
from urllib.parse import urlparse

class Waybackurls:
    def run(self, ctx):
        domain = urlparse(ctx.url).netloc
        api = (
            "https://web.archive.org/cdx/search/cdx"
            f"?url={domain}/*&output=json&fl=orginal&collapse=urlkey"
        )

        urls = []
        try:
            r = requests.get(api, timeout=20)
            for row in r.json()[1:]:
                urls.append(row[0])
        except:
            pass

        return urls