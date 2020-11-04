#/home/rodion/python_virtual/env/bin/python3
import requests

while True:
    text = input()
    requests.post(
        'http://127.0.0.1:5000/send',
        json={'text': text, 'name': 'admin'}
    )
