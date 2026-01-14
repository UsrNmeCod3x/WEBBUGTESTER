from urllib.parse import urlparse, parse_qs

class Context:
    def __init__(self, url, http):
        self.http = http
        self.findings = set()
        self.set_target(url)

    def set_target(self, url):
        self.url = url
        self.parsed = urlparse(url)
        self.params = parse_qs(self.parsed.query)

    def report(self, vuln, detail):
        key = (vuln, detail)
        if key not in self.findings:
            self.findings.add(key)
            print(f"        [{vuln}] {detail}")
