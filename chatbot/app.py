from pymongo import MongoClient
import datetime
from flask import Flask, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.chatbot
collection = db.performance


@app.route('/')
def hello():
    return 'hello world'


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    req = request.get_json(force=True)
    fulfillmentText = ''

    query_result = req.get('queryResult')

    print(query_result)

    # 순위 질문했을 때
    if query_result.get('intent').get('displayName') == 'ask.rank':
        performance = db.rank.find().limit(10)

        for i in performance:
            fulfillmentText += i['performance_rank'] +". " + i['performance_name'] + "\n"

        return {"fulfillmentText": fulfillmentText, "source":'webhook'}

    # 날짜로 질문했을 때
    if query_result.get('intent').get('displayName') == 'ask.date':
        date1 = str(query_result.get('parameters').get('date'))
        dateformat = '%Y-%m-%dT%H:%M:%S+09:00'
        date_obj = datetime.datetime.strptime(date1, dateformat)  # datetime으로 변환
        result = date_obj.strftime("%Y%m%d")  # 쿼리에 사용할 형식의 string으로 변환

        performance = collection.find( {"stdate": result} )
        for i in performance:
            fulfillmentText += i['title']

        if not fulfillmentText:
            return {"fulfillmentText": "해당 공연 정보 없음 ㅠㅠ", "source": 'webhook'}

        return {"fulfillmentText": fulfillmentText, "source": 'webhook'}

    # 제목으로 질문했을 때
    if query_result.get('intent').get('displayName') == 'ask.title':
        result = str(query_result.get('parameters').get('title'))

        if not result:
            return {"fulfillmentText": "해당 공연 정보 없음 ㅠㅠ", "source": 'webhook'}

        performance = collection.find({"title": {"$regex": "^" + result}})

        if not performance:
            return {"fulfillmentText": "해당 공연 정보 없음 ㅠㅠ", "source": 'webhook'}

        for i in performance:
            title = i['title']
            genre = i['genre']

        return {"fulfillmentMessages": [{
            "payload": {
                "line": {
                    "type": "template",
                    "altText": "this is a carousel template",
                    "template": {
                        "type": "carousel",
                        "columns": [
                            {
                                "thumbnailImageUrl": "https://www.kopis.or.kr/upload/pfmPoster/PF_PF132236_160704_142630.gif",
                                "imageBackgroundColor": "#FFFFFF",
                                "title": title,
                                "text": genre,
                                "defaultAction": {
                                    "type": "uri",
                                    "label": "View detail",
                                    "uri": "http://example.com/page/123"
                                },
                                "actions": [
                                    {
                                        "type": "postback",
                                        "label": "공연 예매",
                                        "data": "action=buy&itemid=111"
                                    },
                                    {
                                        "type": "uri",
                                        "label": "자세히 보기",
                                        "uri": "http://example.com/page/111"
                                    }
                                ]
                            },
                            {
                                "thumbnailImageUrl": "https://example.com/bot/images/item1.jpg",
                                "imageBackgroundColor": "#FFFFFF",
                                "title": title,
                                "text": genre,
                                "defaultAction": {
                                    "type": "uri",
                                    "label": "View detail",
                                    "uri": "http://example.com/page/123"
                                },
                                "actions": [
                                    {
                                        "type": "postback",
                                        "label": "공연 예매",
                                        "data": "action=buy&itemid=111"
                                    },
                                    {
                                        "type": "uri",
                                        "label": "자세히 보기",
                                        "uri": "http://example.com/page/111"
                                    }
                                ]
                            },
                        ],
                        "imageAspectRatio": "rectangle",
                        "imageSize": "cover"
                    }},
                "platform": "LINE"
            }}]}

    return {"fulfillmentText": "해당 공연 없음 ㅠ.ㅠ"}


if __name__ == '__main__':
    # port = int(os.getenv('PORT',80))
    app.run(host='0.0.0.0', port=5000)
