from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Home page – lets user choose a room
@app.route('/')
def index():
    return render_template('index.html')

# Room page
@app.route('/room/<room_name>')
def room(room_name):
    user = request.args.get("user", "Guest")
    return render_template('room.html', room_name=room_name, user=user)

# When a user joins
@socketio.on('join')
def handle_join(data):
    room = data['room']
    user = data['user']
    join_room(room)
    send(f"✅ {user} has joined {room}.", room=room)

# When a user sends a message
@socketio.on('message')
def handle_message(data):
    room = data['room']
    msg = data['msg']
    user = data['user']
    send(f"{user}: {msg}", room=room)

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=8000, debug=True)









