ffrom flask import Flask, render_template, request
from flask_socketio import SocketIO, send, join_room
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/room/<room_name>')
def room(room_name):
    user = request.args.get("user", "Guest")
    return render_template('room.html', room_name=room_name, user=user)

@socketio.on('join')
def handle_join(data):
    room = data['room']
    user = data['user']
    join_room(room)
    send(f"✅ {user} has joined {room}.", room=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    msg = data['msg']
    user = data['user']
    send(f"{user}: {msg}", room=room)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port, debug=False)








