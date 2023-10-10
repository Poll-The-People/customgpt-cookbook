import requests
import json
import time
from credentials import credentials

api_endpoint, api_token = credentials()

headers = {
    'Content-type': 'application/json',
    'Authorization': 'Bearer ' + api_token
}

def test_projects():
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
    project_name_created = project_data["project_name"]
    assert project_name_created == project_name
    assert response_create.status_code == 201

    # Update a project
    project_id = project_data["id"]
    project_name = 'test2'
    payload = json.dumps({
        "project_name": project_name
    })

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

    url = api_endpoint + 'projects' + f"/{project_id}"
    update_project = requests.request('POST', url, headers=headers, data=payload)
    assert update_project.status_code == 200
    project_updated_data = json.loads(update_project.text)["data"]
    project_name_updated = project_updated_data["project_name"]
    assert project_name_created != project_name_updated
    assert project_name_updated == project_name

    # Get Project By created project Id and assert updated name
    response = requests.request('GET', url, headers=headers)
    project_data = json.loads(response.text)["data"]
    project_name_get = project_data["project_name"]
    assert project_name_get == project_name
    assert response.status_code == 200

    # Fetch Created project Stat
    url_stats = url + '/stats'
    response = requests.request('GET', url_stats, headers=headers)
    response_stats = json.loads(response.text)["data"]
    assert response.status_code == 200
    assert set(list(response_stats.keys())) == set(
        [
            "pages_found",
            "pages_crawled",
            "pages_indexed",
            "crawl_credits_used",
            "query_credits_used",
            "total_queries",
            "total_words_indexed",
        ]
    )
    list_url = api_endpoint + 'projects'
    response = requests.request('GET', list_url, headers=headers)
    response_list = json.loads(response.text)["data"]
    assert response.status_code == 200
    assert len(response_list) > 0 

    # Delete the project
    response = requests.request('DELETE', url, headers=headers)
    assert response.status_code == 200
