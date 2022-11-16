
from pymongo import MongoClient

import datetime
client = MongoClient("mongodb+srv://hanieminha:performance888@haniemchatbot.pvxxz0o.mongodb.net/test")
db = client.chatbot
collection = db.performance

def ask_date1(date):
    fulfillmentText = ''
    thumbnail=''
    genre=''
    column=[]

    dateformat = '%Y-%m-%dT%H:%M:%S+09:00'
    date_obj = datetime.datetime.strptime(date, dateformat) #datetime으로 변환  

    result = date_obj.strftime("%Y.%m.%d") #쿼리에 사용할 형식의 string으로 변환
    title = collection.find( #db에서 날짜에 해당하는 data찾기
        { "$and":[{"stdate" : {"$lte": result}},{"eddate" : {"$gte": result}}] }, 
        {"_id":0,"title":1,"poster":1,"genre":1}).limit(10)

    
    for i in title:
        #제목에 글자수 제한이 있음. 30넘으면 그냥 출력 pass
        if len(i['title']) > 30:
            continue
        
        fulfillmentText=i['title']
        thumbnail=i['poster']
        genre=i['genre']
        print(fulfillmentText)
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
                "type": "message",
                "label": "세부 정보 보기",
                "text": fulfillmentText+" 세부 정보 알려줘", #누르면 세부정보 message보내지게함
            },
            
            ]
        }
        column.append(col);
                
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
                },
            },
                    
        },
        "platform": "LINE"
        },
        {
        "payload": {
            "line": {
                "type": "template",
                "altText": "This is a buttons template",
                "template": {
                    "type": "buttons",
                    "title": "More information",
                    "text": "더많은 공연이 궁금하신가요?",
                    "defaultAction": {
                    "type": "message",
                    "label": "공연 10개 더보기",
                    "text": "공연 10개 더 보여줘"
                    },
                    "actions": [
                    {
                        "type": "message",
                        "label": "공연 10개 더보기",
                        "text": " 공연 10개 더 보여줘" #누르면 세부정보 message 보내지게함
                    },
                    ]
                },
            },
        },
        "platform": "LINE"
        }
        ],
    }
    
def ask_date2(date1,date2):
    fulfillmentText = ''
    thumbnail=''
    genre=''
    column=[]

    dateformat = '%Y-%m-%dT%H:%M:%S+09:00' 
    date_obj = datetime.datetime.strptime(date1, dateformat) #datetime으로 변환
    date_obj2 = datetime.datetime.strptime(date2, dateformat) #datetime으로 변환  
        

    stDate = date_obj.strftime("%Y.%m.%d") #쿼리에 사용할 형식의 string으로 변환
    edDate = date_obj2.strftime("%Y.%m.%d")
    
    title = collection.find( #db에서 날짜에 해당하는 data찾기
        { "$and":[{"stdate" : {"$gte": stDate}},{"eddate" : {"$lte": edDate}}] }, 
        {"_id":0,"title":1,"poster":1,"genre":1}).limit(10)
    
    for i in title:
        #제목에 글자수 제한이 있음. 30넘으면 그냥 출력 pass
        if len(i['title'])> 30:
            continue
        
        fulfillmentText=i['title']
        thumbnail=i['poster']
        genre=i['genre']
        
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
            "type": "message",
            "label": "View Detail",
            "text": fulfillmentText+" 세부 정보 알려줘", #누르면 세부정보 message보내지게함
        },
        {
            "type": "uri",
            "label": "View detail",
            "uri": "http://example.com/page/111"
        }
        ]
        }
        column.append(col);
        
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
                    },
                },
                        
            },
            "platform": "LINE"
            },
            {
            "payload": {
                "line": {
                    "type": "template",
                    "altText": "This is a buttons template",
                    "template": {
                        "type": "buttons",
                        "title": "More information",
                        "text": "더많은 공연이 궁금하신가요?",
                        "defaultAction": {
                        "type": "message",
                        "label": "공연 10개 더보기",
                        "text": "공연 10개 더 보여줘"
                        },
                        "actions": [
                        {
                            "type": "message",
                            "label": "공연 10개 더보기",
                            "text": " 공연 10개 더 보여줘" #누르면 세부정보 message 보내지게함
                        },
                        ]
                    },
                },
            },
            "platform": "LINE"
            }
            ],
        }
        
