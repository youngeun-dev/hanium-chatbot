from pymongo import MongoClient
import requests
import json
import xmltodict

# MongoDb 연결
client = MongoClient('localhost', 27017)
db = client.chatbot

# open api 인증키
service_key = "301c5f567d2f41298b70c98de5d89b09"

# 공연 목록 DB에 insert
params = {
    'service': service_key,
    'stdate': 20200101,
    'eddate': 202201231,
    'rows': 10,
    'cpage': 1
}
res = requests.get(url='http://www.kopis.or.kr/openApi/restful/pblprfr', params=params)
data = res.text
jsonString = json.dumps(xmltodict.parse(data), indent=4, ensure_ascii=False)

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

    perfo = {'perfoID': perfoID, 'title': title, 'stdate': stdate, 'eddate': eddate,
             'genre': genre, 'concerthall': concerthall}

    # db.performance.insert_one(perfo)
performances = list(db.performance.find({}, {'_id': False}))
print(performances)

# ------------------------------------------------------------------------------------------------
# 예매 순위 DB에 insert
params = {
    'service' : service_key,
    'ststype' : "day",
    'date' : 20220718
}

res = requests.get(url="http://kopis.or.kr/openApi/restful/boxoffice", params=params)
data = res.text
jsonString = json.dumps(xmltodict.parse(data), indent=4, ensure_ascii=False)

rankList = json.loads(jsonString)
rankArray = rankList["boxofs"]["boxof"]

for rank in rankArray:
    perfoID = rank["mt20id"]
    perfoName = rank["prfnm"]
    perfoRank = rank["rnum"]

    rank = { 'performance_id' : perfoID, 'performance_name' : perfoName, 'performance_rank' : perfoRank }
    # db.rank.insert_one(rank)

ranks = list(db.rank.find({}, {'_id': False}))
print(ranks)
print((db.rank.find_one({'performance_rank':"2"}))['performance_name'])