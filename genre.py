from pymongo import MongoClient

client = MongoClient("mongodb+srv://hanieminha:performance888@haniemchatbot.pvxxz0o.mongodb.net/test")
db = client.chatbot
collection = db.performance

def ask_genre(find_genre):
    fulfillmentText = ''
    thumbnail=''
    genre=''
    column=[]
    title = collection.find({"genre": find_genre},{"_id":0,"title":1,"poster":1,"genre":1}).limit(10)
        
    for i in title:
        fulfillmentText = i['title']
        thumbnail = i['poster']
        genre = i['genre']

        col = {
            "thumbnailImageUrl": thumbnail,
            "imageBackgroundColor": "#FFFFFF",
            "title": fulfillmentText,
            "text": genre,
            "defaultAction": {
                "type": "uri",
                "label": "View detail",
                "uri": "http://example.com/page/123"
            },
            "actions": [
                {
                    "type": "postback",
                    "label": "More Information",
                    "data": "action=buy&itemid=111"
                },
                {
                    "type": "uri",
                    "label": "View detail",
                    "uri": "http://example.com/page/111"
                }
            ]
        }
        column.append(col);

    # print(fulfillmentText)
    # print(thumbnail)
    # print(genre)
    return {
        "fulfillmentMessages": [
            {
                "payload": {
                    "line": {
                        "type": "template",
                        "altText": "this is a carousel template",
                        "template": {
                            "type": "carousel",
                            "columns": column,
                            "imageAspectRatio": "rectangle",
                            "imageSize": "cover"
                        }
                    }

                },
                "platform": "LINE"
            },
        ]
    }
