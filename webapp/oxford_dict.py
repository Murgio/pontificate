import requests
import json

from auth import create_auth
auth = create_auth()

class Word:
    def __init__(self, name, auth):
        self.name = name
        self.language = "en-gb"
        self._auth = auth

    def _url(self):
        return f"https://od-api.oxforddictionaries.com/api/v2/entries/{self.language}/{self.name.lower()}"

    def get_json(self):
        self.r = requests.get(self._url(), headers=self._auth)

print("code {}\n".format(r.status_code))
print("text \n" + r.text)
print("json \n" + json.dumps(r.json()))
