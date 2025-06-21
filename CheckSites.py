import json
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
jsonURL = "https://raw.githubusercontent.com/MR-VL/sherlock2/master/sherlock_project/resources/data.json"


def fetch_json(url):
    try:
        response = requests.get(url, timeout = 10)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        print(f"Error fetching JSON: {e}")
        return None

def check_site_status(site_name, site_info):
    url_main  = site_info.get("urlMain")

    if not url_main:
        return site_name, {"status": "No url main", "status_code": None}

    try:
        response = requests.head(url_main, allow_redirects=True, timeout = 5)
        status_code = response.status_code
        #some sites do not support HEAD, use GET instead as last resort
        if status_code >= 400 or status_code == 405:
            response = requests.get(url_main, allow_redirects=True, timeout = 5)
            status_code = response.status_code

        is_active = 200 <= status_code < 400
        status = "Active" if is_active else "Inactive"
        return site_name, {"status": status, "status_code": status_code}

    except requests.RequestException:
        return site_name, {"status": "Unreachable", "status_code": None}

if __name__ == "__main__":
    site_data = fetch_json(jsonURL)
    if not site_data:
        exit("Failed to load JSON from GitHub.")

    site_status = {}

    with ThreadPoolExecutor(max_workers = 100) as executor:
        future_site = {executor.submit(check_site_status, site, info) : site for site, info in site_data.items() if site != "$schema"}
        for future in as_completed(future_site):
            site, result = future.result()
            site_status[site] = result
            print(f"{site}: {result['status']} (Status Code: {result['status_code']})")
    with open('site_status_results_from_github.json', 'w') as outfile:
        json.dump(site_status, outfile, indent=4)
    print("\nResults saved to 'site_status_results_from_github.json'")

