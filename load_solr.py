import os
import requests
import logging
import json

# read each file in ./data/lessons, convert to a dict to sent to solr
path = "./data/lessons"
collection = "sermons"

create_collection_response = requests.post(
    url="http://localhost:8983/api/collections",
    headers={"Content-Type": "application/json"},
    json={
            "name":collection,
            "numShards": 1,
            "replicationFactor": 1
        }
)

if create_collection_response.status_code >= 400:
    logging.error(create_collection_response.text)
    raise Exception(create_collection_response.text)

schema_response = requests.post(
    url=f"http://localhost:8983/api/collections/{collection}/schema",
    headers={"Content-Type": "application/json"},
    json={
            "add-field": [
                {
                    "name": "title",
                    "type": "text_general",
                    "multiValued": False,
                },
                {
                    "name": "content",
                    "type": "text_general",
                    "multiValued": False
                }
            ]
        }
)

if schema_response.status_code >= 400:
    logging.error(schema_response.text)
    raise Exception(schema_response.text)

for f in os.listdir(path):
    with open(os.path.join(path, f), 'r') as fp:
        content = fp.read()

    doc = {
        "title": f,
        "content": content
    }

    logging.info(f"Uploading {f}")
    repsonse = requests.post(
        url=f"http://localhost:8983/api/collections/{collection}/update?commit=true",
        headers={"Content-Type": "application/json"},
        json=doc
    )

    if repsonse.status_code >= 400:
        logging.error(f"{f} -> Error: {repsonse.status_code} {repsonse.text}")
    else:
        logging.info(f"{f} -> {repsonse.status_code}")
