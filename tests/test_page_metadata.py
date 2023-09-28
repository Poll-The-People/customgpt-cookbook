import requests
import json

from credentials import credentials

api_endpoint, api_token = credentials()

headers = {
    'Content-type': 'application/json',
    'Authorization': 'Bearer ' + api_token
}

def test_project_metadata():
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
    url = api_endpoint + 'projects' + f"/{project_id}" + '/pages'
    project_pages = requests.request('GET', url, headers=headers)
    assert project_pages.status_code == 200
    data = json.loads(project_pages.text)['data']
    page_id = data['pages']['data'][0]['id']
    url = api_endpoint + 'projects' + f"/{project_id}" + '/pages' + f"/{page_id}" +'/metadata'
    page_metadata = requests.request('GET', url, headers=headers)
    assert page_metadata.status_code == 200
    data = json.loads(page_metadata.text)['data']
    title = data['title']
    payload = json.dumps({
        "title": "Test2"
    })
    response = requests.request('PUT', url, headers=headers, data=payload)
    assert response.status_code == 200
    page_metadata = requests.request('GET', url, headers=headers)
    assert page_metadata.status_code == 200
    data = json.loads(page_metadata.text)['data']
    assert title != data['title']