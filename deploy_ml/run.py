import json
import requests
import pandas as pd

"""Setting the headers to send and accept json responses
"""
header = {'Content-Type': 'application/json', \
                  'Accept': 'application/json'}

# header = {'Content-Type' : 'text/html'}


"""Reading test batch
"""
df = pd.read_csv('data/test.csv', encoding="utf-8-sig")
# df = df.head()

"""Converting Pandas Dataframe to json
"""
data = df.to_json(orient='records')

"""POST <url>/predict
"""
# On posting this request you get a response from the server 
resp = requests.post("http://127.0.0.1:5000/",data = json.dumps(data),headers= header)

print(resp.status_code)
# print(resp.text)

