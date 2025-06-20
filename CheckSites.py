import json
import requests
import time

jsonURL = "https://raw.githubusercontent.com/MR-VL/sherlock2/master/sherlock_project/resources/data.json"


def fetch_json(url):
    try:
        response = requests.get(url, timeout = 10)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        print(f"Error fetching JSON: {e}")
        return None

def check_site_status(url):
    print("hello")

if __name__ == "__main__":
    site_data = fetch_json(jsonURL)
    if not site_data:
        exit("Failed to load JSON from GitHub.")

    results = {}

    for site_name, site_info in site_data.items():
        if site_name == "$schema":
            continue

        url_main = site_info["urlMain"]

        if not url_main:
            results["site_name"] = {"status": "No url_main", "status_code": None}
            continue

        is_active, status_code = check_site_status(url_main)

        if status_code is None:
            results["site_name"] = {"status": "Unreachable", "status_code": None}
        else:
            results[site_name] = {"status": "Active" if is_active else "Inactive", "status_code": status_code}


        print(f"{site_name}: {results[site_name]['status']} (Status Code: {results[site_name]['status_code']})")
        time.sleep(0.5)

    with open('site_status_results_from_github.json', 'w') as outfile:
        json.dump(results, outfile, indent=4)
    print("\nResults saved to 'site_status_results_from_github.json'")

