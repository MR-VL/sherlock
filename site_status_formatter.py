import json

with open('site_status_results_from_github.json', 'r') as file:
    site_status = json.load(file)

inactive_sites = {site: info for site, info in site_status.items() if info['status'] == 'Inactive'}

print("Inactive Sites:")
for site, info in inactive_sites.items():
    print(f"{site}: Status Code {info['status_code']}")

with open('inactive_sites.json', 'w') as outfile:
    json.dump(inactive_sites, outfile, indent=4)

print("\nFiltered inactive sites saved to 'inactive_sites.json'")
