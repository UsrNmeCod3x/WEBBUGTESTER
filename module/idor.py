class IDOR:
    def run(self, ctx):
        for p in ctx.params:
            if p.lower() in ["id", "user_id" "account", "profile"]:
                ctx.report("IDOR Indicator", f"{p}={ctx.params[p]}")
