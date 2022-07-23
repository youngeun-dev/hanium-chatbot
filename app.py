from flask import Flask
from pymongo import MongoClient
import requests
import json
import xmltodict

client = MongoClient('localhost', 27017)
db = client.chatbot
collection = db.performance


url = 'http://www.kopis.or.kr/openApi/restful/pblprfr'
service_key="66122ee6118e42288de23913ed3f24fb"

params = {  
    'service' : service_key,
        'stdate' : 20220101,
        'eddate' : 20221231,
        'rows' : 4000,
        'cpage': 2
}

res = requests.get(url=url,params=params)
data = res.text
jsonString = json.dumps(xmltodict.parse(data), indent=4, ensure_ascii = False)
 

perfList = json.loads(jsonString)
perfos = perfList["dbs"]
perfosarray = perfos['db']

for perf in perfosarray:
    perfoID = perf["mt20id"]
    title = perf["prfnm"]
    stdate = perf["prfpdfrom"]
    eddate = perf["prfpdto"]
    genre = perf["genrenm"] 
    concerthall = perf["fcltynm"]

    perfo = {'perfoID':perfoID,'title':title, 'stdate':stdate ,'eddate':eddate ,
         'genre':genre, 'concerthall':concerthall}
    
    db.performance.insert_one(perfo)
    
