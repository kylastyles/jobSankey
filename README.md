## Job Search Sankey

### About
This project gives a way to display meaningful data about the job hunting activities of an individual.

Produce a Sankey diagram from a structured document containing the columns: ["date", "position", "status"], where "status" will hold enums such as: ["Applied", "Interview, "Rejected", "Accepted"].

The structured data for this project was stored in a Google Sheet. As such, the scripts/data-extractor.py file is written specifically for Google Sheet data pulls. As an intermediary step to reduce unnecessary API calls, the data is written out to a csv file. Devs that wish to skip the Google Sheet step may start with a .csv for the scripts/data-loader.py instead.  

```commandline
# example.csv
Date,Position,Status
2/3/24,Job_1,Applied
2/3/24,Job_2,Applied
2/6/24,Job_1,Rejected
2/7/24,Job_2,Interview_1
2/10/24,Job_3,Applied
2/13/24,Job_2,Rejected
```

#### Inspirations: 
https://github.com/ashvinbhutekar/Sankey/blob/main/sankey%404.txt

https://github.com/msquinn/vega-demo/blob/main/lib/spec.json

### How to Run
1. Create a virtual environment `python3 -m venv venv`
2. Edit and paste the environment variables listed below to the bottom of the venv/bin/activate file
3. Activate the virtual environment `source venv/bin/activate`
3. Open a terminal at the root of this directory, and then run the following commands:
- `make up` to stand up Docker containers
- *`make pull` to pull data from a Google Sheet (*optional, else create your own csv)
- `make push` to load documents in ElasticSearch
- `make dashboard` to create the Kibana dashboard

View the dashboard by opening a browser to localhost:5601/app/dashboards

![Screenshot 2024-05-07 at 10.19.03 PM.png](..%2F..%2FDesktop%2FScreenshot%202024-05-07%20at%2010.19.03%E2%80%AFPM.png)

### Environment Variables
Change values as needed.
```
export ELASTIC_PASSWORD=<pick something good and strong>
export KIBANA_PASSWORD=<pick something good and strong>
export STACK_VERSION=8.13.1
export CLUSTER_NAME=<whatever, eg: "docker-cluster">
export ES_PORT=9200
export KIBANA_PORT=5601
export DATA_FILE=<location of your csv for reading/writing data, eg: "/path/to/data/JobEvents.csv">

# vvv optional vvv
export DATA_URL=<your google sheet link, eg: "https://docs.google.com/spreadsheets/your-special-google-hash">
export SHEET_NAME=<your google sheet name, eg: "MyJobEvents">
export CRED_FILE=<location of your google api json credential file, eg: "/path/to/creds/service_account.json">
# ^^^ optional ^^^
```
Devs skipping the Google Sheet step will not need the optional env vars. 

It is good practice to also `unset` all env vars in the deactivate() section of the venv/bin/activate file:
```commandline
deactivate () {
    unset ELASTIC_PASSWORD
    unset KIBANA_PASSWORD
    unset STACK_VERSION
    unset CLUSTER_NAME
    unset ES_PORT
    unset KIBANA_PORT
    unset DATA_URL
    unset SHEET_NAME
    unset CRED_FILE
    unset DATA_FILE
    
    # ...
```

### Cleaning Up
1. `make down` to stop the Docker containers.
2. `deactivate` to leave the virtual environment.