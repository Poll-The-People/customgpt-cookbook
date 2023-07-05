import requests
import json
import random
import string
from credentials import credentials

api_endpoint, api_token = credentials()

headers = {
    'Content-type': 'application/json',
    'Authorization': 'Bearer ' + api_token
}

def test_users():
    project_name = 'Example ChatBot using Sitemap'
    sitemap_path = 'https://adorosario.github.io/small-sitemap.xml'

    payload = json.dumps({
        "project_name": project_name,
        "sitemap_path": sitemap_path
    })

    url = api_endpoint + 'user'

    user_response = requests.request('GET', url, headers=headers)
    user_data = json.loads(user_response.text)["data"]
    user_id = user_data["id"]

    assert user_response.status_code == 200
    name = user_data['name']


    payload = json.dumps({
        "name": ''.join(random.choices(string.ascii_uppercase))
    })
    update_user = requests.request('POST', url, headers=headers, data=payload)
    assert update_user.status_code == 200
    data = json.loads(update_user.text)['data']
    assert data['name'] != name
