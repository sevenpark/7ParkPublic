#!/usr/bin/env python3

# Interactive script to help users to traverse through AKM API
# User needs to install `requests`

import requests
import json
from urllib.parse import urljoin
from pprint import pprint

CLIENT_ID = ''
CLIENT_SECRET = ''
DOMAIN = 'https://api.7parkdata.com/'
HEADER = {'content-type': 'application/json'}


def instruction():
    print('Select function:')
    print('Search for company by company name -- 1')
    print('Search for metrics by company id -- 2')
    print('Search for entities by company id & metric id -- 3')
    print('Search for queries by company id, metric id, and entity id -- 4')
    print('Search for time series data by metric id, entity id, metric periodicity, and country name (optional) -- 5')
    print('Search for forecasts by company name -- 6')
    print('Search for forecast by company id, metric id, and entity id -- 7')
    print('Search for forecast history by company id, metric id, and entity id -- 8')
    print('Search for forecast snapshot by company id, metric id, and entity id -- 9')
    print('Exit -- 10')
    selection = input('Type in number: ')
    return selection


def company_name_to_id(company_name):
    print('Using company name: %s to retrieve company id' % company_name)
    url = urljoin(DOMAIN, 'companies')
    payload = {'search': '%s' % company_name}

    response = requests.get(url, headers=headers, params=payload)
    if response.status_code == 200:
        print('-'*40)
        for r in response.json()['results']:
            print("%s [%s]" % (r['company_name'], r['company_id']))
        print('-'*40)
    else:
        print(response.content)


def company_id_to_metrics(company_id):
    print('Using company id: %s to retrieve metric id' % company_id)
    url = DOMAIN + 'company/%s/metrics' % company_id
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print('-'*40)
        for r in response.json()['results']:
            print('%s [%s] -- %s' % (r['metric_name'], r['metric_id'], r['metric_description']))
        print('-'*40)
    else:
        print(response.content)


def metric_id_to_entities(company_id, metric_id):
    print('Using company id: %s & metric id: %s to retrieve entity id' % (company_id, metric_id))
    url = DOMAIN + 'company/%s/metric/%s/entities' % (company_id, metric_id)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print('-'*40)
        for r in response.json()['results']:
            print('%s [%s]' % (r['entity_name'], r['entity_id']))
        print('-'*40)
    else:
        print(response.content)


def get_queries(company_id, metric_id, entity_id):
    print('Using company id: %s, metric id: %s, & entity id: %s to retrieve queries' %
          (company_id, metric_id, entity_id))
    url = DOMAIN + 'company/%s/metric/%s/entity/%s/queries' % (company_id, metric_id, entity_id)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print('-'*40)
        for r in response.json()['queries']:
            pprint(r)
        print('-'*40)
    else:
        print(response.content)


def get_time_series(metric_id, entity_id, metric_periodicity, country_name=''):
    print('Using metric id: %s, & entity id: %s %s' % (metric_id, entity_id, 'and country name: %s' % country_name if country_name else ''))
    url = DOMAIN + 'data'
    payload = {'entity_id': entity_id,
               'metric_periodicity': metric_periodicity,
               'metric_id': metric_id}
    if country_name:
        payload['country_name'] = country_name
    response = requests.get(url, headers=headers, params=payload)
    if response.status_code == 200:
        print('-'*40)
        for r in response.json()['data']:
            pprint(r)
        print('-'*40)
    else:
        print(response.content)


def get_forecasts(company_name):
    print('Using company_name: %s to get forecasts')
    url = DOMAIN + 'forecasts'
    payload = {'search': '%s' % company_name}
    response = requests.get(url, headers=headers, params=payload)
    if response.status_code == 200:
        print('-'*40)
        for r in response.json()['results']:
            print(r)
        print('-'*40)
    else:
        print(response.content)


def get_forecast(company_id, metric_id, entity_id):
    print('Using company id: %s, metric id: %s, & entity id: %s to retrieve forecast' %
          (company_id, metric_id, entity_id))
    url = DOMAIN + 'company/%s/metric/%s/entity/%s/forecast' % (company_id, metric_id, entity_id)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        print('-'*40)
        print("forecast_metric_name: %s" % json_response['forecast_metric_name'])
        for r in json_response['data']:
            pprint(r)
        print('-'*40)
    else:
        print(response.content)


def get_forecast_history(company_id, metric_id, entity_id):
    print('Using company id: %s, metric id: %s, & entity id: %s to retrieve forecast' %
          (company_id, metric_id, entity_id))
    url = DOMAIN + 'company/%s/metric/%s/entity/%s/forecast/history' % (company_id, metric_id, entity_id)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        print('-'*40)
        print("description: %s" % json_response['description'])
        for r in json_response['data']:
            pprint(r)
        print('-'*40)
    else:
        print(response.content)


def get_forecast_snapshot(company_id, metric_id, entity_id, data_through=None):
    print('Using company id: %s, metric id: %s, & entity id: %s to retrieve forecast' %
          (company_id, metric_id, entity_id))
    url = DOMAIN + 'company/%s/metric/%s/entity/%s/forecast/snapshot' % (company_id, metric_id, entity_id)
    if data_through:
        url += f'?data_through={data_through}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        print('-'*40)
        pprint(json_response)
        print('-'*40)
    else:
        print(response.content)


if __name__ == '__main__':
    if not CLIENT_ID or not CLIENT_SECRET:
        print('You do not have your client id and secret set in script.')
        print('You can enter the id and secret acquired from https://account.7parkdata.com/#/akm_key/')
        print('in the script, under "CLIENT_ID" and "CLIENT_SECRET" if you want to avoid '
              'being asked for them every time.')
        client_id = input('please enter your client id: ')
        client_secret = input('please enter your client secret: ')
    else:
        client_id = CLIENT_ID
        client_secret = CLIENT_SECRET

    token_url = urljoin(DOMAIN, 'oauth/token')
    global headers
    headers = HEADER
    payload = {'client_id': client_id, 'client_secret': client_secret}
    response = requests.post(token_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        token = response.json()['access_token']
        headers['Authorization'] = 'Bearer ' + token
    else:
        print('Cannot get token with given client id and secret. Aborting......')
        exit(1)
    selection = instruction()
    while selection:

        if str(selection) == '1':
            company_name = input('Please choose company name of the company you want to search: ')
            company_name_to_id(company_name)
        elif str(selection) == '2':
            company_id = input('Please choose company id of the company you want to search: ')
            company_id_to_metrics(company_id)

        elif str(selection) == '3':
            company_id = input('Please choose company id of the company you want to search: ')
            metric_id = input('Please choose metric id of the metric you want to search: ')
            metric_id_to_entities(company_id, metric_id)

        elif str(selection) == '4':
            company_id = input('Please choose company id of the company you want to search: ')
            metric_id = input('Please choose metric id of the metric you want to search: ')
            entity_id = input('Please choose entity id of the entity you want to search: ')
            get_queries(company_id, metric_id, entity_id)

        elif str(selection) == '5':
            metric_id = input('Please choose metric id of the metric you want to search: ')
            entity_id = input('Please choose entity id of the entity you want to search: ')
            metric_periodicity = input('Please choose metric periodicity you want to search: ').title()
            country_name = input('Please choose country you want to search (can leave empty if none): ')
            get_time_series(metric_id, entity_id, metric_periodicity, country_name)

        elif str(selection) == '6':
            company_name = input('Please choose company name of the company you want to search: ')
            get_forecasts(company_name)

        elif str(selection) == '7':
            company_id = input('Please choose company id of the company you want to search: ')
            metric_id = input('Please choose metric id of the metric you want to search: ')
            entity_id = input('Please choose entity id of the entity you want to search: ')
            get_forecast(company_id, metric_id, entity_id)

        elif str(selection) == '8':
            company_id = input('Please choose company id of the company you want to search: ')
            metric_id = input('Please choose metric id of the metric you want to search: ')
            entity_id = input('Please choose entity id of the entity you want to search: ')
            get_forecast_history(company_id, metric_id, entity_id)

        elif str(selection) == '9':
            company_id = input('Please choose company id of the company you want to search: ')
            metric_id = input('Please choose metric id of the metric you want to search: ')
            entity_id = input('Please choose entity id of the entity you want to search: ')
            data_through = input('Filter by data_through, give all data which data_through greater than giving date. '
                                 '(Format: YYYY-MM-DD  Default: None)')
            get_forecast_snapshot(company_id, metric_id, entity_id, data_through)

        elif str(selection) == '10':
            print('Goodbye!')
            exit(0)
        else:
            print('Function not implemented')
            exit(1)

        print('Do you want to do anything else?\n')
        selection = instruction()

