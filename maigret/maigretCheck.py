import json
import requests
from requests.exceptions import RequestException
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_url(name, url):
    try:
        response = requests.get(url, timeout=(5, 10))  # connect timeout=5s, read timeout=10s
        return (name, {
            "urlMain": url,
            "reachable": True,
            "status_code": response.status_code,
            "reason": response.reason
        })
    except requests.exceptions.Timeout:
        return (name, {
            "urlMain": url,
            "reachable": False,
            "error": "Timeout"
        })
    except requests.exceptions.ConnectionError:
        return (name, {
            "urlMain": url,
            "reachable": False,
            "error": "Connection error"
        })
    except RequestException as e:
        return (name, {
            "urlMain": url,
            "reachable": False,
            "error": str(e)
        })


def main():
    print("Loading JSON file...")
    with open('sites.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    sites = data.get('sites', {})
    print(f"Found {len(sites)} sites.")

    results = {}

    with ThreadPoolExecutor(max_workers=1000) as executor:
        futures = []
        for name, info in sites.items():
            url = info.get('urlMain')
            if url:
                futures.append(executor.submit(check_url, name, url))

        for future in as_completed(futures):
            name, result = future.result()
            results[name] = result

    for site, result in results.items():
        print(f"{site}:")
        for k, v in result.items():
            print(f"  {k}: {v}")
        print()

    with open('site_check_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)
    print("Results saved to site_check_results.json")

if __name__ == "__main__":
    main()
