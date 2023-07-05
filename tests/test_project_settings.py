import requests
import json

from credentials import credentials

api_endpoint, api_token = credentials()

headers = {
    'Content-type': 'application/json',
    'Authorization': 'Bearer ' + api_token
}

def test_project_settings():
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
    url = api_endpoint + 'projects' + f"/{project_id}" + '/settings'
    project_settings = requests.request('GET', url, headers=headers)
    assert project_settings.status_code == 200
    data = json.loads(project_settings.text)['data']
    assert data['default_prompt'] == 'Ask Me Anything ...'

    # Update Project Settings
    if 'Content-type' in headers.keys():
        del headers['Content-type']
    default_prompt = 'Example ChatBot using Sitemap'
    payload = {
        "default_prompt": (None, default_prompt),
        "example_questions[0]": (None, 'Test1'),
        "example_questions[1]": (None, 'Test2'),
        "response_source": (None, "default"),
        "chatbot_msg_lang": (None, "ur")
    }
    update_project_settings = requests.request('POST', url, headers=headers, files=payload)
    assert update_project_settings.status_code == 200
    data = json.loads(update_project_settings.text)['data']
    assert data['updated'] == True

    # Check for updated settings
    project_settings = requests.request('GET', url, headers=headers)
    assert project_settings.status_code == 200
    data = json.loads(project_settings.text)['data']
    assert data['default_prompt'] == default_prompt
    assert data['example_questions'] == ['Test1', 'Test2']
    assert data['response_source'] == 'default'
    assert data['chatbot_msg_lang'] == 'ur'

