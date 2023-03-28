import logging

import azure.functions as func
import json
import requests
import os
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime
import uuid



def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        
        settings = {
            'host': os.environ.get('ACCOUNT_HOST', 'https://openhack1.documents.azure.com:443/'),
            'master_key': os.environ.get('ACCOUNT_KEY', '0JioMkUJKHyzq5qoQ4DtGZkcxX2p0dvdE3hJf0WtLaOHok3l1gQbxOLj6m0hHmMUzynghuy43eEZACDb6A5jrg=='),
            'database_id': os.environ.get('COSMOS_DATABASE', 'ToDoList'),
            'container_id': os.environ.get('COSMOS_CONTAINER', 'Items'),
        }

        HOST = settings['host']
        MASTER_KEY = settings['master_key']
        DATABASE_ID = settings['database_id']
        CONTAINER_ID = settings['container_id'] 

        client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
        db = client.get_database_client(DATABASE_ID)
        container = db.get_container_client(CONTAINER_ID)
    


        logging.info('Python HTTP trigger function processed a request.')
        x=requests.get ('https://serverlessohapi.azurewebsites.net/api/GetProducts')
        products=json.loads(x.text)

        x=requests.get ('https://serverlessohapi.azurewebsites.net/api/GetUsers')
        users=json.loads(x.text)



        rating1 = req.params.get('rating')


        item_list = list(container.read_all_items(max_item_count=10))
        ratingfound=False
        for k in item_list:
            if 'rating' in k.keys():
                if k['rating']==rating1:
                    return func.HttpResponse(f"success, {k}",status_code=200)
                    ratingfound=True
                    break
        if not ratingfound:
            return func.HttpResponse(f"Hello, rating  {rating1} not found.",status_code=200)
                

        
    except Exception as e:
        return func.HttpResponse(f"Hello, {e} not found.",status_code=200)  