from flask import Flask, jsonify
import os

import openai
from flask import Flask, request, render_template, jsonify, json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# 设置OpenAI API key
openai.api_key = "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"

systemSetting = {'role': 'system', 'content': '你是一个用萌萌的语气说话的助手'}
allMessages = [systemSetting]

# 基本chat
def chat(allMessages):  #定义一个函数，以便后面反复调用
    if type(allMessages)!=list:
        allMessages = [systemSetting,{'role': 'user', 'content': allMessages}]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=allMessages,)
    response_format = {
        'role': response['choices'][0]['message']['role'],
        'content': response['choices'][0]['message']['content'],
    }
    return {'response_format':response_format,'tokens':response['usage']['total_tokens']}

# 一轮对话
# def chat_round(ask):
#     allMessages.append({'role': 'user', 'content': ask})
#     answer = chat(allMessages)
#     allMessages.append(answer['response_format'])
#     print(answer['tokens'],answer['response_format']['content'])

@app.route('/fastChat', methods=['POST','GET'])
def fast_chat():
    if request.method == 'POST':
        question = json.loads(request.data.decode('utf-8'))['question']
        answer = chat(question)
        return {"answer":answer}
    if request.method == 'GET':
        question = request.args.get('q')
        answer = chat(question)
        return answer['response_format']['content']

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
