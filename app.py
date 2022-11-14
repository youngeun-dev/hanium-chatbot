from pymongo import MongoClient
from flask import Flask, request
app = Flask(__name__)
from rank import ask_rank
import datetime

client = MongoClient("mongodb+srv://hanieminha:performance888@haniemchatbot.pvxxz0o.mongodb.net/test")
db = client.chatbot
collection = db.performance

@app.route('/')
def hello():
    return 'hello world'
   
@app.route('/webhook',methods=['GET','POST'])
def webhook():
    req = request.get_json(force=True)
    fulfillmentText = ''
    thumbnail=''
    genre=''
    column=[]
    query_result = req.get('queryResult')
    
     # 순위 질문했을 때
    if query_result.get('intent').get('displayName') == 'ask.rank':
        return ask_rank()
    
    if query_result.get('action') == 'ask.date' : #날짜로 질문했을 때
            
        date = str(query_result.get('parameters').get('date-time'))
        if date.startswith('{') :
            date1 = str(query_result.get('parameters').get('date-time').get('startDate'))
            date2 = str(query_result.get('parameters').get('date-time').get('endDate')) 

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
                
        else : 
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
                        "text": "공연 10개 더 보여줘" #누르면 세부정보 message보내지게함
                    },
                    ]
                 },
            },
        },
        "platform": "LINE"
        }
        ],
    }


    # 장르로 질문했을 때
    if query_result.get('action') == 'ask.genre':  # 장르로 질문했을 때
        find_genre = str(query_result.get('parameters').get('genre'))
        title = list(db.performance.find({"genre": find_genre},{"_id": False}))

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

    # 제목으로 질문했을 때
    if query_result.get('action') == 'ask.title':
        result = str(query_result.get('parameters').get('title'))

        perfid = collection.find(  # db에서 제목에 해당하는 data찾기
            {"title": result})

        for i in perfid:
            fulfillmentText = "Title:" + i['title'] + ", ID:" + i['perfoID'] + ", Genre: " + i['genre']

        print(fulfillmentText)
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
                                        "thumbnailImageUrl": "https://example.com/bot/images/item1.jpg",
                                        "imageBackgroundColor": "#FFFFFF",
                                        "title": "this is menu",
                                        "text": "description",
                                        "defaultAction": {
                                            "type": "uri",
                                            "label": "View detail",
                                            "uri": "http://example.com/page/123"
                                        },
                                        "actions": [
                                            {
                                                "type": "postback",
                                                "label": "Buy",
                                                "data": "action=buy&itemid=111"
                                            },
                                            {
                                                "type": "postback",
                                                "label": "Add to cart",
                                                "data": "action=add&itemid=111"
                                            },
                                            {
                                                "type": "uri",
                                                "label": "View detail",
                                                "uri": "http://example.com/page/111"
                                            }
                                        ]
                                    },
                                    {
                                        "thumbnailImageUrl": "https://example.com/bot/images/item2.jpg",
                                        "imageBackgroundColor": "#000000",
                                        "title": "this is menu",
                                        "text": "description",
                                        "defaultAction": {
                                            "type": "uri",
                                            "label": "View detail",
                                            "uri": "http://example.com/page/222"
                                        },
                                        "actions": [
                                            {
                                                "type": "postback",
                                                "label": "Buy",
                                                "data": "action=buy&itemid=222"
                                            },
                                            {
                                                "type": "postback",
                                                "label": "Add to cart",
                                                "data": "action=add&itemid=222"
                                            },
                                            {
                                                "type": "uri",
                                                "label": "View detail",
                                                "uri": "http://example.com/page/222"
                                            }
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
    
if __name__ =='__main__':
    #port = int(os.getenv('PORT',80))
    app.run(host='0.0.0.0',port=5000)



