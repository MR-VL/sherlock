import json
import requests
import time

jsonURL = "https://raw.githubusercontent.com/MR-VL/sherlock2/master/sherlock_project/resources/data.json"


def fetchJson(url):
    print("hello")

def checkSiteStatus(url):
    print("hello")

if __name__ == "__main__":
    siteData = fetchJson(jsonURL)
    if not siteData:
        exit("Failed to load JSON from GitHub.")

    results = {}

    for siteName, siteInfo in siteData.items():
        if siteName == "$schema":
            continue
