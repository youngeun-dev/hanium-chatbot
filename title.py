from pymongo import MongoClient

client = MongoClient("mongodb+srv://hanieminha:performance888@haniemchatbot.pvxxz0o.mongodb.net/test")
db = client.chatbot
collection = db.performance


def ask_title(title):
    fulfillmentText = ''
    thumbnail=''
    genre=''
    stdate=''
    eddate=''
    time=''
    concerthall=''
    price=''
    text=''
    perfid = collection.find( #db에서 제목에 해당하는 data찾기
            { "title" : title },{"_id":0,"title":1,"stdate":1, "eddate":1,"poster":1,"genre":1,"concerthall":1,"price":1,"time":1})

    for i in perfid:
        fulfillmentText = i['title']
        thumbnail=i['poster']
        genre = i['genre']
        stdate=i['stdate']
        eddate=i['eddate']
        time=i['time']
        concerthall=i['concerthall']
        price=i['price']
    
    text = "날짜 : "+ stdate + "~" +eddate + "\n시간 : " + time + "\n콘서트홀 : " + concerthall+  "\n가격 : " + price
    
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
        {
                "payload": {
                    "line": {
                        "type": "text",
                        "text": text
                    },
                },
                "platform": "LINE"
            },
      
        ]
    };