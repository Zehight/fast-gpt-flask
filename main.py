import os
import requests as pyrequests
import tiktoken
from flask import Flask, request, render_template, jsonify, json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# 一轮对话
# def chat_round(ask):
#     allMessages.append({'role': 'user', 'content': ask})
#     answer = chat(allMessages)
#     allMessages.append(answer['response_format'])
#     print(answer['tokens'],answer['response_format']['content'])



def chat(question):
    result = pyrequests.post('https://api.miragari.com/fast/fastChat',json={'question':question})
    return json.loads(result.text)

def getTokenNum(messages):
    if type(messages) != list:
        messages = [{'role': 'user', 'content': messages}]
    num_tokens = 0
    for message in messages:
        num_tokens += 4
        for key, value in message.items():
            num_tokens += len(tiktoken.encoding_for_model("gpt-3.5-turbo-0301").encode(value))
            if key == "name":
                num_tokens += -1
    num_tokens += 2
    return str(num_tokens)

@app.route('/', methods=['POST','GET'])
def fast_chat():
    if request.method == 'POST':
        question = json.loads(request.data.decode('utf-8'))['question']
        return chat(question)
    if request.method == 'GET':
        question = request.args.get('q')
        if question is None:
            return '欢迎哦~'
        else:
            return chat(question)

@app.route('/getToenNum', methods=['POST','GET'])
def get_token_num():
    if request.method == 'POST':
        question = json.loads(request.data.decode('utf-8'))['question']
        return getTokenNum(question)
    if request.method == 'GET':
        question = request.args.get('q')
        if question is None:
            return '0'
        else:
            return getTokenNum(question)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
