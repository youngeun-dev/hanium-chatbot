from pymongo import MongoClient
import datetime

client = MongoClient('localhost', 27017)
db = client.chatbot
collection = db.performance


def ask_date(query_result):
    fulfillmentText = ''

    date1 = str(query_result.get('parameters').get('date'))
    dateformat = '%Y-%m-%dT%H:%M:%S+09:00'
    date_obj = datetime.datetime.strptime(date1, dateformat)  # datetime으로 변환
    result = date_obj.strftime("%Y%m%d")  # 쿼리에 사용할 형식의 string으로 변환

    performance = collection.find({"stdate": result})
    for i in performance:
        fulfillmentText += i['title']

    if not fulfillmentText:
        return {"fulfillmentText": "해당 공연 정보 없음 ㅠㅠ", "source": 'webhook'}

    return {"fulfillmentText": fulfillmentText, "source": 'webhook'}
