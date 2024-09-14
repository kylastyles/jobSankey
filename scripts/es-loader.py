#!/usr/bin/env/python3.12

import csv
import hashlib
import json
import os

from datetime import datetime
from elasticsearch import Elasticsearch, exceptions


'''
This script will create the ElasticSearch index if not exists, 
and save each row of the data file as an ElasticSearch doc,
using a custom _id to prevent dupes on multiple re-runs.

It will also create "No_Response" entries for jobs that
have not moved beyond the "Applied" status. 
Previously saved "No_Response" entries are deleted on re-run
and then recalculated anew. 

Run with `python3 es-loader.py`
'''

# elasticsearch necessities
INDEX = "job_events"
MAP = {
    "properties": {
        "date": {
            "type": "date",
            "format": "MM/dd/yy||yyyy-M-dd||epoch_millis"
        },
        "position": {"type": "keyword"},
        "status": {"type": "keyword"}
    }
}

es_client = Elasticsearch('http://0.0.0.0:9200')


# data necessities
headers = ["date", "position", "status"]
accepted_statuses = {
    "Applied",
    "Interview_1",
    "Turned_down",
    "No_response",
    "Rejected",
    "Recruiter_chat_1",
    "Recruiter_chat_2",
    "Recruiter_chat_3"
}
# TODO add "Interview_2", "Interview_3", "Recruiter_chat_4"

try:
    DATA_FILE = os.environ["DATA_FILE"]
except KeyError as e:
    print(f"ERROR: missing necessary env var from environment: {e}")
    raise SystemExit(1)


# --- create index if needed ---
try:
    es_client.search(index=INDEX)
except exceptions.NotFoundError:
    es_client.indices.create(index=INDEX, mappings=MAP)
finally:
    print(f"*** Index '{INDEX}' exists with {es_client.count(index=INDEX)['count']} docs ***\n\n")

# --- write data to es ---
no_response_dict = {}
with open(DATA_FILE) as infile:
    reader = csv.DictReader(infile, fieldnames=headers, dialect='excel')
    # skip header row
    next(reader)
    for row in reader:
        # --- clean data ---
        row_status = row["status"].lower().capitalize().replace(' ', '_')
        row["status"] = row_status
        # reject statuses from the raw data that have not yet been incorporated into the visualization
        # (can always re-run again once the status is incorporated)
        if row_status not in accepted_statuses:
            print(f"Skipping row containing {row_status} status")
            continue
        row_date = datetime.strptime(row["date"], "%m/%d/%y")
        row["date"] = datetime.strftime(row_date, "%Y-%m-%d")
        print(row)

        # add row to a dictionary needed later; newer statuses will replace previous entries
        no_response_dict[row["position"]] = row_status
        # hash each row as its _id to prevent dupes
        doc_id = hashlib.md5((row["date"] + row["position"] + row_status).encode()).hexdigest()
        # create elasticsearch entry
        resp = es_client.index(index=INDEX, id=doc_id, document=json.dumps(row))
        print(resp)

# --- create No_Response entries based on no_response_dict ---
print("Dropping stale No_response entries...\n\n")
resp = es_client.delete_by_query(index=INDEX, body={"query": {"term": {"status": "No_response"}}})
print(resp)

print("Calculating fresh No_response entries...\n\n")
for k, v in no_response_dict.items():
    # for entries that never got past Applied state
    if v == "Applied":
        row = {"date": datetime.now().strftime('%Y-%m-%d'), "position": k, "status": "No_response"}
        print(row)
        doc_id = hashlib.md5((row["date"] + row["position"] + row["status"]).encode()).hexdigest()
        resp = es_client.index(index=INDEX, id=doc_id, document=json.dumps(row))
        print(resp)

# --- make new data immediately available for search ---
es_client.indices.refresh(index=INDEX)
