from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.chatbot
collection = db.performance


def ask_rank():
    fulfillmentText = ''
    column = []

    performance = db.rank.find().limit(10)

    for i in performance:
        fulfillmentText += i['performance_rank'] + ". " + i['performance_name'] + "\n"
        col = {
            "thumbnailImageUrl": "https://example.com/bot/images/item1.jpg",
            "imageBackgroundColor": "#FFFFFF",
            "title": i['performance_name'],
            "text": i['performance_rank'],
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

    return {
        "fulfillmentMessages": [
            {
                "payload": {
                    "line": {
                        "type": "text",
                        "text": fulfillmentText[:-1]
                    },
                },
                "platform": "LINE"
            },
            {"payload": {
                "line": {
                    "type": "template",
                    "altText": "this is a carousel template",
                    "template": {
                        "type": "carousel",
                        "columns": column,
                        "imageAspectRatio": "rectangle",
                        "imageSize": "cover"
                    }
                },

            },
                "platform": "LINE"}

        ]
    }
