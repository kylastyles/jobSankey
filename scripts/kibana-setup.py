import requests

'''
To import the dashboard and visualization. 

Run with `python3 kibana-setup.py`

View with a browser at localhost:5601/app/dashboards
'''

try:
    r = requests.post("http://0.0.0.0:5601/api/saved_objects/_import",
                      files={'file': open('export.ndjson', 'rb')},
                      headers={"kbn-xsrf": "true"})
    print(r)

except Exception as e:
    print(e)