from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, join_room
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Home page – lets user choose a room
@app.route('/')
def index():
    return render_template('index.html')

# Room page – chat interface
@app.route('/room/<room_name>')
def room(room_name):
    user = request.args.get("user", "Guest")
    return render_template('room.html', room_name=room_name, user=user)

# Handle joining a room
@socketio.on('join')
def handle_join(data):
    room = data['room']
    user = data['user']
    join_room(room)
    send(f"✅ {user} has joined {room}.", room=room)

# Handle sending messages
@socketio.on('message')
def handle_message(data):
    room = data['room']
    msg = data['msg']
    user = data['user']
    send(f"{user}: {msg}", room=room)

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT if set
    socketio.run(app, host="0.0.0.0", port=port)











