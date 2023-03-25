import os
import requests as pyrequests
from flask import Flask, request, render_template, jsonify, json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# 一轮对话
# def chat_round(ask):
#     allMessages.append({'role': 'user', 'content': ask})
#     answer = chat(allMessages)
#     allMessages.append(answer['response_format'])
#     print(answer['tokens'],answer['response_format']['content'])

def chat(question):
    result = pyrequests.post('https://api.miragari.com/fast/fastChat',json={'question':question})
    return json.loads(result.text)['answer']

@app.route('/fastChat', methods=['POST','GET'])
def fast_chat():
    if request.method == 'POST':
        question = json.loads(request.data.decode('utf-8'))['question']
        answer = chat(question)
        return {'answer':answer}
    if request.method == 'GET':
        question = request.args.get('q')
        answer = chat(question)
        return answer['response_format']['content']

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
