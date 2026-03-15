import urllib.request

try:
    response = urllib.request.urlopen('http://127.0.0.1:8000/')
    print(f"Success! Status Code: {response.status}")
except Exception as e:
    print(f"Error accessing local server: {e}")
