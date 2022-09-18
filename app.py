import rank, date, title
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello():
    return 'hello world'


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    req = request.get_json(force=True)

    query_result = req.get('queryResult')
    print(query_result)

    # 순위 질문했을 때
    if query_result.get('intent').get('displayName') == 'ask.rank':
        return rank.ask_rank()

    # 날짜로 질문했을 때
    if query_result.get('intent').get('displayName') == 'ask.date':
        return date.ask_date(query_result)

    # 제목으로 질문했을 때
    if query_result.get('intent').get('displayName') == 'ask.title':
        return title.ask_title(query_result)

    return {"fulfillmentText": "해당 공연 없음 ㅠ.ㅠ"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)