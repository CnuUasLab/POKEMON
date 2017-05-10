from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, disconnect

app = Flask(__name__, static_folder='')
io = SocketIO(app)

clients = []

@app.route('/')
def index():
    return render_template('client.html', async_mode=None)

@io.on('connected')
def connected():
    print "%s connected" % (request.namespace.socket.sessid)
    clients.append(request.namespace)

@io.on('disconnect')
def disconnect():
    print "%s disconnected" % (request.namespace.socket.sessid)
    clients.remove(request.namespace)

def hello_to_random_client():
    import random
    from datetime import datetime
    if clients:
        k = random.randint(0, len(clients)-1)
        print "Saying hello to %s" % (clients[k].socket.sessid)
        clients[k].emit('message', "Hello at %s" % (datetime.now()))

if __name__ == '__main__':
    import thread, time
    thread.start_new_thread(lambda: io.run(app), ())

    while True:
        time.sleep(1)
        hello_to_random_client()
