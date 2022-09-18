from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.chatbot
collection = db.performance


def ask_title(query_result):
    result = str(query_result.get('parameters').get('title'))
    column = []

    if not result:
        return {"fulfillmentText": "해당 공연 정보 없음 ㅠㅠ", "source": 'webhook'}

    performance = collection.find({"title": {"$regex": "^" + result}})

    if not performance:
        return {"fulfillmentText": "해당 공연 정보 없음 ㅠㅠ", "source": 'webhook'}

    for i in performance:
        title = i['title']
        genre = i['genre']
        col = {
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
        }
        column.append(col)

    return {"fulfillmentMessages": [{
        "payload": {
            "line": {
                "type": "template",
                "altText": "this is a carousel template",
                "template": {
                    "type": "carousel",
                    "columns": column,
                    "imageAspectRatio": "rectangle",
                    "imageSize": "cover"
                }},
            "platform": "LINE"
        }}]}