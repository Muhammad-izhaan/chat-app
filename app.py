from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit
import secrets
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    session['username'] = username
    emit('user_joined', {'username': username}, broadcast=True)

@socketio.on('message')
def handle_message(data):
    username = session.get('username', 'Anonymous')
    emit('message', {
        'username': username,
        'message': data['message']
    }, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
