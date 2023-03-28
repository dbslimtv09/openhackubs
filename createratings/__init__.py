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


        userId = req.params.get('userId')
        productId = req.params.get('productId')
        locationName = req.params.get('productId')
        rating = req.params.get('rating')
        userNotes = req.params.get('userNotes')

        userok=False
        for k in users:
            if k['userId']==userId:
                userok=True
                break

        productok=False
        for k in products:
            if k['productId']==productId:
                productok=True
                break

    #    if userok and productok:
    #        write to db 

        if not productok:
            return func.HttpResponse(f"Hello, {productId} not found.",status_code=200)
        else:
            if not userok:
                return func.HttpResponse(f"Hello, {userId} not found.",status_code=200)
            else:
                payload1 = {
                              "id": str(uuid.uuid4()),
                              "userId": userId,
                              "productId": productId,
                              "timestamp": str(datetime.datetime.now()),
                              "locationName": locationName,
                              "rating": rating,
                              "userNotes": userNotes
                            }
                
                container.create_item(body=payload1)
                return func.HttpResponse(f"success, {payload1}",status_code=200)
        
    except Exception as e:
        return func.HttpResponse(f"Hello, {e} not found.",status_code=200)  