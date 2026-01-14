class ReflectedXSS:
    payload = "<svg/onload=alert(1)>"

    def run(self, ctx):
        for p in ctx.params:
            params = ctx.params.copy()
            params[p] = self.payload
            test = ctx.url.split("?")[0] + "?" + "&".join(
                f"{k}={v}" for k, v in params.items()
            )

            r = ctx.http.get(test)
            if self.payload in r.text:
                ctx.report("Reflected XSS", p)