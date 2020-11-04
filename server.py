#/home/rodion/python_virtual/env/bin/python3
from flask import Flask, request, abort
from datetime import datetime
import time 
app = Flask(__name__)

db = [
    {
        'text': 'Привет',
        'name': 'Nick',
        'time': time.time()
    }, {
        'text': 'Привет, Nick',
        'name': 'Jane',
        'time': time.time()
    }, {
        'text': 'Как дела?',
        'name': 'Nick',
        'time': time.time()
    }
]

@app.route("/")

def hello():
    return("hi <a href='/status'>Статистика</a>")

@app.route("/status")
def status():
    return {
        'name': 'post_msg',
        'messages_count': 500,
        'server_time': time.time(),
        'status': True,
        'time': datetime.now().isoformat()
    }

@app.route("/send", methods=['POST'])
def send_message():
    if not isinstance(request.json, dict):
        return abort(400)
    
    text = request.json.get('text')
    name = request.json.get('name')
    
    if not isinstance(text, str) or not isinstance(name, str):
        return abort(400)
    if text == '' or name == '':
        return abort(400)
    db.append({
        'text': text,
        'name': name,
        'time': time.time()
    })
    return {'ok':True}

@app.route("/messages")
def get_messages():
    if 'after' in request.args:
        try:
            after = float(request.args['after'])
        except:
            print('error')
            return abort(400)
    else:
        after = 0 
    filtered_db = []
    for message in db:
        if message['time'] > after:
            filtered_db.append(message)
            if len(filtered_db) >= 100:
                break
    return {'messages': filtered_db}

app.run()