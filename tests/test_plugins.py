import requests
import json
import time
import random
import string
from credentials import credentials

api_endpoint, api_token = credentials()

headers = {
    'Content-type': 'application/json',
    'Authorization': 'Bearer ' + api_token
}

def test_plugins():
    # Create a project
    project_name = 'Example ChatBot using Sitemap'
    sitemap_path = 'https://adorosario.github.io/small-sitemap.xml'

    payload = json.dumps({
        "project_name": project_name,
        "sitemap_path": sitemap_path
    })

    url = api_endpoint + 'projects'

    response_create = requests.request('POST', url, headers=headers, data=payload)
    project_data = json.loads(response_create.text)["data"]
    project_id = project_data["id"]

    # wait for chat active
    is_chat_active = 0
    json_project = {}
    while not is_chat_active:
        get_url = api_endpoint +'projects' + f"/{project_id}"
        response = requests.request('GET', get_url, headers=headers)
        json_project = json.loads(response.text)["data"]
        is_chat_active = json_project['is_chat_active']
        time.sleep(5)

    assert json_project['is_chat_active'] == 1


    # Create Project plugin
    plugin_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
    payload = json.dumps({
      "model_name": plugin_name,
      "human_name": "The Indoor Plants",
      "keywords": "Indoor plants, Gardening, Trusted information.",
      "description": "Trusted information about indoor plants and gardening.",
      "is_active": True
	})

    url = api_endpoint + 'projects' + f"/{project_id}/" + 'plugins'
    create_plugin = requests.request('POST', url, headers=headers, data=payload)
    data = json.loads(create_plugin.text)["data"]
    model_name = data['model_name']

    assert model_name == plugin_name
    assert create_plugin.status_code == 201


    # Update a plugin
    plugin_name2 = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
    payload = json.dumps({
      "model_name": plugin_name2,
      "human_name": "The Indoor Plants",
      "keywords": "Indoor plants, Gardening, Trusted information.",
      "description": "Trusted information about indoor plants and gardening.",
      "is_active": True
	})

    url = api_endpoint + 'projects' + f"/{project_id}/" + 'plugins'
    update_plugin = requests.request('PUT', url, headers=headers, data=payload)
    data = json.loads(update_plugin.text)["data"]
    model_name = data['model_name']

    assert model_name == plugin_name2
    assert update_plugin.status_code == 200


    url = api_endpoint + 'projects' + f"/{project_id}/" + 'plugins'
    list_plugin = requests.request('GET', url, headers=headers)
    data = json.loads(list_plugin.text)["data"]
    assert list_plugin.status_code == 200
    assert data['model_name'] == plugin_name2