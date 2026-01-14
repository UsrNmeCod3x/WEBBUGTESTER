import sys
import re
from recon.subdomains import get_subdomains
from module.wayback import Waybackurls
from module.js_endpoint import JSEndpoint
from module.open_redirect import OpenRedirect
from module.xss import ReflectedXSS
from module.sqli import SQLi
from module.idor import IDOR
from module.ssrf import SSRF
from module.headers import SecurityHeaders
from core.context import Context
from core.http import HTTPClient


def validate_domain(domain):
    """Validate the input domain format"""
    if not domain or len(domain) < 3:
        return False
    # Simple validation: check for valid characters and format
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9](\.[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9])*\.*$'
    return bool(re.match(pattern, domain))


def main():
    try:
        wildcard = input("Enter wildcard domain (e.g. *.example.com): ").strip()
        
        if not wildcard:
            print("[-] Error: Domain cannot be empty")
            sys.exit(1)
            
        if not validate_domain(wildcard.replace("*.", "")):
            print(f"[-] Error: Invalid domain format '{wildcard.replace('*.', '')}'")
            sys.exit(1)
            
        domain = wildcard.replace("*.", "")
        
        print(f"\n[*] Enumerating subdomains for {domain}")
        subdomains = get_subdomains(domain)
        
        if not subdomains:
            print(f"[-] No subdomains found for {domain}")
            sys.exit(0)
        
        print(f"[+] Found {len(subdomains)} subdomains")
        
        http = HTTPClient()
        
        vuln_modules = [
            OpenRedirect(),
            ReflectedXSS(),
            SQLi(),
            IDOR(),
            SSRF(),
            SecurityHeaders()
        ]
        
        total_processed = 0
        for i, sub in enumerate(subdomains, 1):
            print(f"\n[{i}/{len(subdomains)}] Processing subdomain: {sub}")
            try:
                ctx = Context(f"https://{sub}", http)
                
                # 1️⃣ Collect endpoints
                print(f"    [*] Collecting endpoints for {sub}...")
                wayback_urls = Waybackurls().run(ctx)
                js_urls = JSEndpoint().run(ctx)
                
                # 2️⃣ Merge & deduplicate
                all_endpoints = set(wayback_urls + js_urls)
                
                print(f"    [+] Total unique endpoints: {len(all_endpoints)}")
                
                # 3️⃣ Run vulnerability checks
                for j, url in enumerate(all_endpoints, 1):
                    try:
                        ctx.set_target(url)
                        for module in vuln_modules:
                            try:
                                module.run(ctx)
                            except Exception as e:
                                print(f"    [-] Error running {module.__class__.__name__} on {url}: {str(e)}")
                    except KeyboardInterrupt:
                        print("\n[!] Scan interrupted by user")
                        sys.exit(0)
                    except Exception as e:
                        print(f"    [-] Error processing endpoint {url}: {str(e)}")
                        continue
                
                total_processed += 1
                print(f"    [+] Completed processing {sub}")
                
            except KeyboardInterrupt:
                print("\n[!] Scan interrupted by user")
                sys.exit(0)
            except Exception as e:
                print(f"    [-] Error processing subdomain {sub}: {str(e)}")
                continue
        
        print(f"\n[*] Scan completed. Processed {total_processed}/{len(subdomains)} subdomains")
        
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"[-] Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
