from pymongo import MongoClient
from flask import Flask, request
app = Flask(__name__)

import datetime

client = MongoClient('localhost', 27017)
db = client.chatbot
collection = db.performance

@app.route('/')
def hello():
    return 'hello world'
   

@app.route('/webhook',methods=['GET','POST'])
def webhook():
  req = request.get_json(force=True)
  fulfillmentText = ''
  
  query_result = req.get('queryResult')
 
   
  if query_result.get('action') == 'ask.date' : #날짜로 질문했을 때
    date1 = str(query_result.get('parameters').get('date-time'))  
    dateformat = '%Y-%m-%dT%H:%M:%S+09:00' 
    date_obj = datetime.datetime.strptime(date1, dateformat) #datetime으로 변환  

    result=date_obj.strftime("%Y%m%d") #쿼리에 사용할 형식의 string으로 변환
    
    title = collection.find( #db에서 날짜에 해당하는 data찾기
        { "$and":[{"stdate" : {"$lte": result}},{"eddate" : {"$gte": result}}] }, 
        {"_id":0,"title":1})
   
    
    for i in title:
        fulfillmentText+=i['title']+','

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
}

    

if __name__ =='__main__':
    #port = int(os.getenv('PORT',80))
    app.run(host='0.0.0.0',port=5000)



