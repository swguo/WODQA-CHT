# Opening JSON file
import json
import pandas as pd
f = open('data/wiki_for_pyserini-tiny.json')
 
data = json.load(f)

json_title=[]
for i in data:
  json_title.append({"id":i["id"],"title":i["title"]}) 

pd.DataFrame(json_title).to_csv('data/wiki_entity.csv',index=None)
f.close()