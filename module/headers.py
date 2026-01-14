class SecurityHeaders:
    def run(self, ctx):
        r = ctx.http.get(ctx.url)
        for h in [
            "Content-Security-Policy",
            "X-Frame-Options",
            "Strict-Transport-Security",
        ]:
            if h not in r.headers:
                ctx.report("Missing Headers", h)
