import re
from urllib.parse import urljoin
class JSEndpoint:
    JS_REJEX = r'src=["\']([^"\']+)["\']'
    API_REJEX = r'["\'](/api[^"\']+)["\']'

    def run(self, ctx):
        endpoints = []

        try:
            r = ctx.http.get(ctx.url)
        except:
            return endpoints

        js_files = re.findall(self.JS_REJEX, r.text)

        for js in js_files:
            js_url = urljoin(ctx.url, js)
            endpoints.extend(self.extract_from_js(ctx, js_url))

        print(f"   ↳ JS endpoints: {len(endpoints)}")
        return endpoints

    def extract_from_js(self, ctx, js_url):
        found = []
        try:
            r = ctx.http.get(js_url)
        except:
            return found

        found += re.findall(self.API_REJEX, r.text)
        return found
