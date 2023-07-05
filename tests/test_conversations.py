import time
import requests
import json
from sseclient import SSEClient
from credentials import credentials

api_endpoint, api_token = credentials()

headers = {
    'Content-type': 'application/json',
    'Authorization': 'Bearer ' + api_token
}

def test_conversations():
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
    conversation_data = json.loads(create_conversation.text)["data"]
    session_id = conversation_data['session_id']
    assert conversation_data['name'] == name
    assert create_conversation.status_code == 201

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

    specific_url = url + f"/{session_id}"
    name = 'Test Converasation 2'
    payload = json.dumps({
        "name": name
    })
    print(specific_url)
    response = requests.request('PUT', specific_url, headers=headers, data=payload)
    assert response.status_code == 200
    updated_conversation_data = json.loads(response.text)["data"]
    assert updated_conversation_data['name'] == name


    # Get Project By created project Id and assert updated name
    response = requests.request('GET', url, headers=headers)
    response_conversation = json.loads(response.text)["data"]
    assert response.status_code == 200
    assert response_conversation['data'][0]['name'] == name
    assert len(response_conversation['data']) > 0

    # send streaming message
    prompt = "Who is Tom Brady"
    # set stream to 1 to get a streaming response
    stream = 1
    message_url = api_endpoint + 'projects/' + str(project_id) + '/conversations/' + str(session_id) + '/messages'
    payload = json.dumps({
        "prompt": prompt,
        "stream": stream
    })
    stream_response = requests.post(message_url, stream=False, headers=headers, data=payload)
    assert stream_response.status_code == 200

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

    # Fetch Created project messages
    response = requests.request('GET', message_url, headers=headers)
    response_messages = json.loads(response.text)["data"]
    assert response.status_code == 200



