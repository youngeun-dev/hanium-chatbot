from pymongo import MongoClient

client = MongoClient("mongodb+srv://hanieminha:performance888@haniemchatbot.pvxxz0o.mongodb.net/test")
db = client.chatbot
collection = db.performance

def ask_title(title):
    fulfillmentText = ''
    thumbnail=''
    genre=''
    
    perfid = collection.find( #db에서 제목에 해당하는 data찾기
            { "title" : title },{"_id":0,"title":1,"poster":1,"genre":1})

    for i in perfid:
        fulfillmentText = i['title']
        thumbnail=i['poster']
        genre = i['genre']

    return { 
        "fulfillmentMessages": [
        {
        "payload": {
            "line": { 
                "type": "template",
                "altText": "this is a carousel template",
                "template": {
                    "type": "carousel",
                    "columns": [
                    {
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
                        "type": "uri",
                        "label": "View Poster",
                        "uri": thumbnail
                    },
                    {
                        "type": "postback",
                        "label": "View detail",
                        "data": "action=add&itemid=111"
                    },
                    ]
                    }
                    ],
                "imageAspectRatio": "rectangle",
                "imageSize": "cover"
                }
            }
                    
        },
        "platform": "LINE"
        },
        ]
    };