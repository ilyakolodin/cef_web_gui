from flask import Flask
from cefpython3 import cefpython as cef
import sys
import threading
from werkzeug.serving import make_server
import random

pin = ''.join([str(random.randint(0, 9)) for i in range(4)])

class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

app = Flask(__name__)
@app.route("/" + pin)
def hello_world():
    return "<p>Hello, World!</p>"


def main():
    global server
    sys.excepthook = cef.ExceptHook
    cef.Initialize()
    cef.CreateBrowserSync(url="http://127.0.0.1:5000/" + pin, window_title="Hello World!")
    cef.MessageLoop()
    server.shutdown()
    cef.Shutdown()
     

if __name__ == '__main__':
    global server
    print(pin)
    server = ServerThread(app)
    t2 = threading.Thread(target=main)
    server.start()
    t2.start()
    
    