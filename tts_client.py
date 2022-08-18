import requests
import json
import sys, base64

#url = 'http://localhost:5000/speech'
url = 'http://localhost:8080/speech'

payload = {
    "speech": "Hello, szia, szevasz! Van nálatok terasz?"
}

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

para = {'speech': "\"ez egy árvíztűrő tükörfúrógép\""}

r = requests.get(url, headers=headers, params=para)
#r = requests.post(url, json = payload)
encoded_mp3_dict = json.loads(r.text)
encoded_mp3 = encoded_mp3_dict['speech']

print(encoded_mp3_dict)
print(encoded_mp3)
print(type(encoded_mp3))


b_str = encoded_mp3.encode()
# print("UTF-8 encoded: ")
# print(b_str)
c = base64.b64decode(b_str)

try:
    file = open('speech_client.mp3', 'wb')
    file.write(c)
    file.close()
except:
    print('Something went wrong!')
    sys.exit(0)


