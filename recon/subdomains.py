import requests

def get_subdomains(domains):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    subs = set()

    try:
        data = requests.get(url, timeout=20).json()
        for entry in data:
            for sub in entry["name_value"].split("/n"):
                if "*" not in sub:
                    subs.add(sub.strip())
    except:
        pass

    return sorted(subs)