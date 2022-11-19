from pymongo import MongoClient

client = MongoClient("mongodb+srv://hanieminha:performance888@haniemchatbot.pvxxz0o.mongodb.net/test")
db = client.chatbot
collection = db.rank

#RANK DB에서 10위까지 찾아서 출력
def ask_rank():
    fulfillmentText = ''
    column = []
    title=''
    performance = db.rank.find().limit(10)

    for i in performance:
        title=i['title']
        fulfillmentText += i['rank'] + ". " + i['title'] + "\n"
        col = {
            "thumbnailImageUrl": i['poster'],
            "imageBackgroundColor": "#FFFFFF",
            "title": i['title'],
            "text": i['rank'],
            "defaultAction": {
                "type": "uri",
                "label": "View detail",
                "uri": "http://example.com/page/123"
            },
            "actions": [
                {
                    "type": "message",
                    "label": "공연 세부정보 알아보기",
                    "text": title + " 정보 알려줘"
                },
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