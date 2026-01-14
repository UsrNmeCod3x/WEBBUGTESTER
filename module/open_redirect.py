from urllib.parse import urlencode, urlunparse

class OpenRedirect:
    def run(self, ctx):
        for p in ctx.params:
            if p.lower() in ["url", "next", "redirect", "return"]:
                params = ctx.params.copy()
                params[p] = "https://evil.com"
                text = urlunparse(ctx.parsed._replace(query=urlencode(params, doseq=true)))

                r = ctx.http.get(text, allow_redirects=false)
                if "Location" in r.headers:
                    ctx.report("Open Redirect", test)