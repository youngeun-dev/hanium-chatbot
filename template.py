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
  thumbnail=''
  genre=''
  column=[]
  query_result = req.get('queryResult')
 
   
  if query_result.get('action') == 'ask.date' : #날짜로 질문했을 때
    date1 = str(query_result.get('parameters').get('date-time'))  
    dateformat = '%Y-%m-%dT%H:%M:%S+09:00' 
    date_obj = datetime.datetime.strptime(date1, dateformat) #datetime으로 변환  

    result=date_obj.strftime("%Y.%m.%d") #쿼리에 사용할 형식의 string으로 변환
    
    title = collection.find( #db에서 날짜에 해당하는 data찾기
        { "$and":[{"stdate" : {"$lte": result}},{"eddate" : {"$gte": result}}] }, 
        {"_id":0,"title":1,"poster":1,"genre":1}).limit(10)
   
    
    for i in title:
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
       
    
    #print(fulfillmentText)
    #print(thumbnail)
    #print(genre)
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

    

if __name__ =='__main__':
    #port = int(os.getenv('PORT',80))
    app.run(host='0.0.0.0',port=5000)



