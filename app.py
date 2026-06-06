from flask import Flask, render_template_string
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, cors_allowed_origins="*")

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Messenger</title>
</head>
<body>
    <h2>💬 Simple Messenger</h2>

    <div id="chat" style="height:300px; overflow:auto; border:1px solid black; padding:10px;"></div>
    <br>

    <input id="msg" placeholder="Type message..." style="width:70%;">
    <button onclick="sendMsg()">Send</button>

<script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
<script>
    var socket = io();

    socket.on("message", function(msg){
        var chat = document.getElementById("chat");
        chat.innerHTML += "<div>" + msg + "</div>";
        chat.scrollTop = chat.scrollHeight;
    });

    function sendMsg(){
        var msg = document.getElementById("msg").value;
        socket.send(msg);
        document.getElementById("msg").value = "";
    }
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@socketio.on("message")
def handle_message(msg):
    send(msg, broadcast=True)

if __name__ == "__main__":
    print("Server running: http://127.0.0.1:5000")
    socketio.run(app, host="0.0.0.0", port=10000)
