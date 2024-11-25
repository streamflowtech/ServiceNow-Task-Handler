import requests
import json
import os
import sys
from dotenv import load_dotenv

def call_handler(method, url, params=None):

    if method == 'get':
        response = requests.get(url, params, auth=auth, headers=headers)
        if response.status_code == 200:
            data = response.json()['result']
            return data
        else:
            return f"Error: {response.status_code}, {response.text}"

def get_open_tasks(assignment_group):

    url = f'{base_url}/sc_task'
    params = {
        'sysparm_fields': 'number,request_item,request_item.name',
        'sysparm_query': f'assignment_group.name={assignment_group}^state=1'
    }
    response = call_handler('get', url, params)
    return response

def get_ritm_short_description(ritm_sys_id):

    url = f'{base_url}/sc_req_item/{ritm_sys_id}'
    params = {
        "sysparm_fields": 'short_description'
    }
    response = call_handler('get', url, params)
    return response

def get_ritm_vars(ritm_sys_id):

    url = f'{base_url}/sc_item_option_mtom'
    params = {
        'sysparm_fields': 'sc_item_option',
        'sysparm_query': f'request_item={ritm_sys_id}'
    }
    response = call_handler('get', url, params)
    return response

def get_ritm_var_data(ritm_var_sys_id):
    
    url = f'{base_url}/sc_item_option/{ritm_var_sys_id}'
    response = call_handler('get', url)
    return response

def get_ritm_var_name(item_option_new_sys_id):

    url = f'{base_url}/item_option_new/{item_option_new_sys_id}'
    params = {'sysparm_fields': 'name'}
    response = call_handler('get', url, params)
    return response

if __name__ == '__main__':

    load_dotenv()

    instance = os.getenv('INSTANCE')
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    assignment_group = os.getenv('ASSIGNMENT_GROUP')

    base_url = f'https://{instance}/api/now/table/'

    headers = {"Accept": "application/json"}
    auth = (username, password)

    tasks = get_open_tasks(assignment_group)

    for task in tasks:

        ritm_sys_id = task['request_item']['value']
        ritm_short_description = get_ritm_short_description(ritm_sys_id)['short_description']
        ritm_vars = get_ritm_vars(ritm_sys_id)

        variables = []

        for ritm_var in ritm_vars:

            ritm_var_data = get_ritm_var_data(ritm_var['sc_item_option']['value'])
            ritm_var_value = ritm_var_data['value']
            ritm_var_name = get_ritm_var_name(ritm_var_data['item_option_new']['value'])['name']

            var_data = {}
            var_data[ritm_var_name] = ritm_var_value
            variables.append(var_data)

        task_data = {}
        task_data['task_number'] = task['number']
        task_data['item_type'] = ritm_short_description
        task_data['task_variables'] = variables

    print(json.dumps(task_data, indent=2))
            
