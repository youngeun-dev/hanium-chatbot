from flask import Flask
from pymongo import MongoClient
import requests
import json
import xmltodict

client = MongoClient('localhost', 27017)
db = client.chatbot
collection = db.performance

url = 'http://www.kopis.or.kr/openApi/restful/pblprfr/'
service_key="66122ee6118e42288de23913ed3f24fb"

params = {  
    'service' : service_key
}

id = collection.find({},{"perfoID":1})
for i in id:
    res = requests.get(url=url+i['perfoID'],params=params)
    perfoid= i['perfoID']

    data = res.text
    jsonString = json.dumps(xmltodict.parse(data),ensure_ascii = False)

    perfList = json.loads(jsonString)
    perfos = perfList["dbs"]
    try:
        perf = perfos["db"]
            
        #poster, 공연 가격, 출연진, 공연시간 받아오기
        poster = perf["poster"]
        price = perf["pcseguidance"]
        cast = perf["prfcast"]
        time = perf["dtguidance"]
        collection.update_one({"perfoID":perfoid},{ "$set": {"poster":poster, "price":price
            , "cast":cast, "time":time}})
    except:
        continue
    

