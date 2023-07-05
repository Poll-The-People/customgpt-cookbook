import requests
import json
import time
from credentials import credentials

api_endpoint, api_token = credentials()


headers = {
    'Content-type': 'application/json',
    'Authorization': 'Bearer ' + api_token
}

def test_citations():
    project_name = 'Example ChatBot using Sitemap'
    sitemap_path = 'https://adorosario.github.io/small-sitemap.xml'

    payload = json.dumps({
        "project_name": project_name,
        "sitemap_path": sitemap_path
    })

    url = api_endpoint + 'projects'

    response_create = requests.request('POST', url, headers=headers, data=payload)
    project_data = json.loads(response_create.text)["data"]
    project_id = project_data['id']
    name = 'Test Converasation'
    payload = json.dumps({
        "name": name
    })

    url = api_endpoint + 'projects' + f"/{project_id}" + '/conversations'
    create_conversation = requests.request('POST', url, headers=headers, data=payload)
    session_id = json.loads(create_conversation.text)['data']['session_id']

    # Wait for project to process
    is_chat_active = 0
    json_project = {}
    while not is_chat_active:
        get_url = api_endpoint +'projects' + f"/{project_id}"
        response = requests.request('GET', get_url, headers=headers)
        json_project = json.loads(response.text)["data"]
        is_chat_active = json_project['is_chat_active']
        time.sleep(5)

    assert json_project['is_chat_active'] == 1

    prompt = "Who is Tom Brady"
    # set stream to 1 to get a streaming response
    stream = 0
    message_url = api_endpoint + 'projects/' + str(project_id) + '/conversations/' + str(session_id) + '/messages'
    payload = json.dumps({
        "prompt": prompt,
        "stream": stream
    })
    stream_response = requests.post(message_url, stream=False, headers=headers, data=payload)
    assert stream_response.status_code == 200
    message_data = json.loads(stream_response.text)['data']
    citation_id = message_data['citations'][0]

    url = api_endpoint + 'projects' + f"/{project_id}" + '/citations/' + str(citation_id)
    project_pages = requests.request('GET', url, headers=headers)
    assert project_pages.status_code == 200
 