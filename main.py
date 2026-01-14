from recon.subdomains import get_subdomains
from modules.wayback import WaybackURLs
from modules.js_endpoints import JSEndpoints
from modules.open_redirect import OpenRedirect
from modules.xss import ReflectedXSS
from modules.sqli import SQLi
from modules.idor import IDOR
from modules.ssrf import SSRF
from modules.headers import SecurityHeaders
from core.context import Context
from core.http import HTTPClient

wildcard = input("Enter wildcard domain (e.g. *.example.com): ")
domain = wildcard.replace("*.", "")

print(f"\n[*] Enumerating subdomains for {domain}")
subdomains = get_subdomains(domain)

http = HTTPClient()

vuln_modules = [
    OpenRedirect(),
    ReflectedXSS(),
    SQLi(),
    IDOR(),
    SSRF(),
    SecurityHeaders()
]

for sub in subdomains:
    print(f"\n[*] Processing subdomain: {sub}")
    ctx = Context(f"https://{sub}", http)

    # 1️⃣ Collect endpoints
    wayback_urls = WaybackURLs().run(ctx)
    js_urls = JSEndpoints().run(ctx)

    # 2️⃣ Merge & deduplicate
    all_endpoints = set(wayback_urls + js_urls)

    print(f"    [+] Total unique endpoints: {len(all_endpoints)}")

    # 3️⃣ Run vulnerability checks
    for url in all_endpoints:
        ctx.set_target(url)
        for module in vuln_modules:
            module.run(ctx)

print("\n[*] Scan completed")
