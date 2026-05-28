import requests

url = "http://localhost:3000/upload-utility/"

files = {
    "file": open("test_utility.csv", "rb")
}

response = requests.post(url, files=files)

print(response.status_code)
print(response.text)