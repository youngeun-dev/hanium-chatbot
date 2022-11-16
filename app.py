from pymongo import MongoClient
from flask import Flask, request
app = Flask(__name__)
from rank import ask_rank
from date import ask_date1,ask_date2
from genre import ask_genre
from title import ask_title

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
            return ask_date2(date1,date2)
        else :
            return ask_date1(date) 
            

    # 장르로 질문했을 때
    if query_result.get('action') == 'ask.genre':  # 장르로 질문했을 때
        find_genre = str(query_result.get('parameters').get('genre'))
        return ask_genre(find_genre)

    # 제목으로 질문했을 때
    if query_result.get('action') == 'ask.title' : #제목으로 질문했을 때
        title = str(query_result.get('parameters').get('title'))  
        return ask_title(title)
        
    
if __name__ =='__main__':
    #port = int(os.getenv('PORT',80))
    app.run(host='0.0.0.0',port=5000)


