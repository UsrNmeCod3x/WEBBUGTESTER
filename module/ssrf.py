class SSRF:
    def run(self, ctx):
        for p in ctx.params:
            if p.lower() in ["url", "dest", "callback", "image"]:
                ctx.report("SSRF Injection", p)