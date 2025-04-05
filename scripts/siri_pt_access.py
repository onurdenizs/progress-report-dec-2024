import requests

API_KEY = "eyJvcmciOiI2NDA2NTFhNTIyZmEwNTAwMDEyOWJiZTEiLCJpZCI6ImQzMDdmODcyMWJjYzQxMjM4NTk2MzlhZDI3ZWE1NjgwIiwiaCI6Im11cm11cjEyOCJ9"  # Replace with your actual API key

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "User-Agent": "my-phd-app",
    "Accept-Encoding": "gzip, deflate, br"
}

url = "https://api.opentransportdata.swiss/la/siri-et"

response = requests.get(url, headers=headers, allow_redirects=True)

if response.status_code == 200:
    print("✅ Success")
    with open("siri_pt_response.xml", "wb") as f:
        f.write(response.content)
    print("📄 Response saved as siri_pt_response.xml")
else:
    print(f"❌ Failed with status {response.status_code}")
    print(response.text)
