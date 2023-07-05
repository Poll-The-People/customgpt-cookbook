import requests
import json
import time
from credentials import credentials
import os
current_script_path = os.path.abspath(__file__)
file_name = 'file/vanka.pdf'
file_path = os.path.join(os.path.dirname(current_script_path), file_name)

api_endpoint, api_token = credentials()

headers = {
    'Content-type': 'application/json',
    'Authorization': 'Bearer ' + api_token
}

def test_sources():
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

    # Add Sitemap path To Project
    new_sitemap_path = 'https://adorosario.github.io/small-sitemap.xml'
    payload = json.dumps({
        "sitemap_path": new_sitemap_path
    })

    url = api_endpoint + 'projects' + f"/{project_id}/" + 'sources'
    create_source = requests.request('POST', url, headers=headers, data=payload)
    data = json.loads(create_source.text)["data"]
    type = data['type']

    assert type == 'sitemap'
    assert create_source.status_code == 201

    del headers['Content-type']
    # Add File To Project
    with open(file_path, 'rb') as file:
        file_content = file.read()
    files = {'file': ('vanka.pdf', file_content)}

    url = api_endpoint + 'projects' + f"/{project_id}/" + 'sources'
    create_source = requests.request('POST', url, headers=headers, files=files)
    data = json.loads(create_source.text)["data"]
    type = data['type']
    assert create_source.status_code == 201
    assert type == 'upload'

    # List Sources
    headers['Content-type'] = 'application/json'
    url = api_endpoint + 'projects' + f"/{project_id}/" + 'sources'
    list_sources = requests.request('GET', url, headers=headers)
    data = json.loads(list_sources.text)["data"]
    assert list_sources.status_code == 200
    assert len(data['sitemaps']) > 0
    assert len(data['uploads']) > 0

    # Delete Source
    source_id = data['sitemaps'][0]['id']
    url = api_endpoint + 'projects' + f"/{project_id}/" + 'sources/' + str(source_id) 
    delete_source = requests.request('DELETE', url, headers=headers)
    assert delete_source.status_code == 200
