import requests
import os
import sys
import time
import argparse

from datetime import datetime
from dotenv import load_dotenv


def notify(message_verbosity, message):

    current_datetime = datetime.now()

    if script_verbosity == 1:
        if message_verbosity == 1:
            print(f'{current_datetime} - {message}')
    if script_verbosity == 2:
        if message_verbosity == 1:
            print(f'{current_datetime} - {message}')
        if message_verbosity == 2:
            print(f'{current_datetime} -  {message}')


def call_handler(method, url, params=None, body=None):

    if method == 'get':
        response = requests.get(url, params, auth=auth, headers=headers)
        if response.status_code == 200:
            data = response.json()['result']
            return data
        else:
            return f"Error: {response.status_code}, {response.text}"
    elif method == 'put':
        response = requests.put(url, json=body, auth=auth, headers=headers)
        if response.status_code == 200:
            data = response.json()['result']
            return data
        else:
            return f"Error: {response.status_code}, {response.text}"


def get_open_tasks(assignment_group):

    url = f'{base_url}/sc_task'
    params = {
        'sysparm_fields': 'number,sys_id,request_item,request_item.cat_item.name',
        'sysparm_query': f'assignment_group.name={assignment_group}^state=1'
    }
    response = call_handler('get', url, params)
    return response


def get_ritm_vars(ritm_sys_id):

    url = f'{base_url}/sc_item_option_mtom'
    params = {
        'sysparm_fields': 'sc_item_option.value,sc_item_option.item_option_new.name',
        'sysparm_query': f'request_item={ritm_sys_id}'
    }
    response = call_handler('get', url, params)
    return response


def set_task_to_wip(task_sys_id):

    url = f'{base_url}/task/{task_sys_id}'
    body = {
        'state': "2",
        'work_notes': 'This task has been picked up by automation'
    }
    response = call_handler('put', url, body=body)
    return response


def update_task_work_notes(task_sys_id, work_note):

    url = f'{base_url}/task/{task_sys_id}'
    body = {
        'work_notes': work_note
    }
    response = call_handler('put', url, body=body)
    return response


def close_task(task_sys_id):

    url = f'{base_url}/task/{task_sys_id}'
    body = {
        'state': "3",
    }
    response = call_handler('put', url, body=body)
    return response


def fulfill_task(task_data):

    return_data = {}

    if task_data['ritm_name'] == 'DNS CNAME Request':

        work_note = 'DNS alias created successfully'
        update_task_work_notes(task_data['task_sys_id'], work_note)

        return_data['result_code'] = 0
        return_data['result_data'] = work_note
        return return_data


def main():

    while True:

        notify(1, 'Getting all open tasks assigned to automation group')
        tasks = get_open_tasks(assignment_group)

        if tasks:
            task_verbiage = "task" if len(tasks) == 1 else "tasks"
            notify(1, f'{len(tasks)} {task_verbiage} retrieved for fulfillment')

            tasks_data = []

            for task in tasks:

                notify(1, f'Working on task {task["number"]}')
                ritm_sys_id = task['request_item']['value']
                ritm_name = task['request_item.cat_item.name']

                notify(1, f'Getting item variables for task {task["number"]}')
                ritm_vars = get_ritm_vars(ritm_sys_id)

                variables = {}

                for ritm_var in ritm_vars:

                    variables[ritm_var['sc_item_option.item_option_new.name']] = ritm_var['sc_item_option.value']

                task_data = {}
                task_data['task_number'] = task['number']
                task_data['task_sys_id'] = task['sys_id']
                task_data['ritm_name'] = ritm_name
                task_data['task_variables'] = variables
                tasks_data.append(task_data)

                notify(1, 'Setting task {task["number"]} to "Work in Progress"')
                set_task_to_wip(task_data['task_sys_id'])

                notify(1, 'Fulfilling task {task["number"]}')
                task_fulfillment = fulfill_task(task_data)

                if task_fulfillment['result_code'] == 0:
                    notify(1, 'Closing task {task["number"]}')
                    close_task(task_data['task_sys_id'])

            notify(1, f'{task_verbiage.capitalize()} fulfilled successfully')

        else:
            notify(1, 'No tasks to fulfill')

        notify(1, 'Sleeping for 10 seconds')
        time.sleep(10)


if __name__ == '__main__':

    my_parser = argparse.ArgumentParser()

    my_parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0
    )

    args = my_parser.parse_args()
    script_verbosity = args.verbose
    if script_verbosity > 2:
        sys.exit('Too much verbosity - exiting.')

    load_dotenv()

    instance = os.getenv('INSTANCE')
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    assignment_group = os.getenv('ASSIGNMENT_GROUP')

    base_url = f'https://{instance}/api/now/table'

    headers = {"Accept": "application/json"}
    auth = (username, password)

    notify(1, 'Starting ServiceNow task handler')

    main()
