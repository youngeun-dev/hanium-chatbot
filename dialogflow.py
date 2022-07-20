from pymongo import MongoClient
import datetime
import json
from flask import Flask, request
app = Flask(__name__)

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
 
  if query_result.get('action') == 'ask.date' :
    date1 = str(query_result.get('parameters').get('date'))
    dateformat = '%Y-%m-%dT%H:%M:%S+09:00'

    date_obj = datetime.datetime.strptime(date1, dateformat)
    result=date_obj.strftime("%Y%m%d")
    
    title = collection.find( 
        { "stdate" : {"$lte": result}},
        {"_id":0,"title":1})

    for i in title:
        fulfillmentText=i['title']
    return {"fulfillmentText": fulfillmentText,
        "source": 'webhook'};

    

if __name__ =='__main__':
    #port = int(os.getenv('PORT',80))
    app.run(host='0.0.0.0',port=5000)