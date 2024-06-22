import requests
import pprint
import json

url = 'https://i.imgur.com/5cZfF7F.jpg'
 
headers = {
    'User-Agent': 'mac:posts_scraper:v1.0 (by u/sinngam_kh)',
    'Accept': 'application/json'
}

# Create a session to manage cookies
session = requests.Session()

response = session.get(url, headers=headers)  # disable SSL verification if needed
with open("media_files/test.png", "wb") as file:
    file.write(response.content)

if response.status_code == 200:
    print('Success:', response)
else:
    print('Failed:', response.status_code, response.text)
