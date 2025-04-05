import requests

# Your app TOKEN here (not the Token Hash!)
API_KEY = "eyJvcmciOiI2NDA2NTFhNTIyZmEwNTAwMDEyOWJiZTEiLCJpZCI6ImRkZmM4NDk4YmQ1YzQ0OTY4MDVkNTdiYmFhN2M5NzY3IiwiaCI6Im11cm11cjEyOCJ9"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "User-Agent": "my-phd-app",  # Just put anything, it's required
    "Accept-Encoding": "gzip, deflate, br"  # optional but good practice
}

params = {
    "evu": "SBBP",  # or one of the allowed ones like THURBO, SOB, etc.
    "operationDate": "2025-04-06",
    "trainNumber": "1518",
    "includeOperationalStops": "false"
}

url = "https://api.opentransportdata.swiss/formations_stop_based"

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    print("✅ Success")
    print(response.json())
    print(response.url)
else:
    print(f"❌ Failed with status {response.status_code}")
    print(response.text)
    print(response.url)
