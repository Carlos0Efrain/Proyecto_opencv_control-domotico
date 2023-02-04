# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
async_mode = None

from flask import Flask, render_template
import socketio
import cv2
import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)



IA=False
sio = socketio.Server(logger=True, async_mode=async_mode)
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
app.config['SECRET_KEY'] = 'secret!'
thread = None


def prenderfoco1():
    ser.write(b'A')
    return False

def prenderfoco2():
    ser.write(b'B')
    return False

def apagarfoco1():
    ser.write(b'Z')
    return False

def apagarfoco2():
    ser.write(b'Y')
    return False

def apagarIA():
    return IA
    
def apagar():
    return True


def prenderIA(mient):
    global IA
    rostros_cascada2 = cv2.CascadeClassifier('haarcascade_eye.xml')
    rostros_cascada = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gestouno = cv2.CascadeClassifier('luz_encender_detector.xml')

    captura = cv2.VideoCapture(0)
    print("funcionando")
    IA=False
    g=0
    g1=0
    g0=0
    while True:
        _, img = captura.read()

        gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        rostros = rostros_cascada.detectMultiScale(gris, 1.2, 5)
        rostros2 = rostros_cascada2.detectMultiScale(gris, 1.2, 5)
        gesto1 = gestouno.detectMultiScale(gris,
                                           scaleFactor = 5,
	                                        minNeighbors = 91,
                                            minSize=(70,78))

        for (x, y, w, h) in rostros:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            g0=g0+1
            if(g0==50):
                prenderfoco1()
                g0=0
        
        for (x, y, w, h) in rostros2:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            g=g+1
            if(g==50):
                prenderfoco2()
                g=0
    
        for (x, y, w, h) in gesto1:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            g1=g1+1
            if(g1==50):
                apagarfoco1()
                apagarfoco2()
                g1=0
       
        cv2.imshow('Inteligencia', img)
        mient=apagarIA()
        if ((cv2.waitKey(10) & 0xFF == 27) or mient):
            break
 
    captura.release()
    



def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        sio.sleep(10)
        count += 1
        sio.emit('my_response', {'data': 'Server generated event'})


@app.route('/')
def index():
    global thread
    if thread is None:
        thread = sio.start_background_task(background_thread)
    return render_template('index.html')

car=False

@sio.event
def my_event(sid, message):
    print(message['data'])
    if(message['data']=='foco1'):
            car=prenderfoco1()
    elif(message['data']=='foco2'):
            prenderfoco2()
    elif(message['data']=='IA'):
        prenderIA(False)
    sio.emit('my_response', {'data': message['data']}, room=sid)

@sio.event
def my_broadcast_event(sid, message):
    global IA
    print(message['data'])
    if(message['data']=='foco1'):
            car=apagarfoco1()
    elif(message['data']=='foco2'):
            car=apagarfoco2()
    elif(message['data']=='IA'):
        IA=apagar()
        message['data']='apagando IA'
    sio.emit('my_response', {'data': message['data']})


@sio.event
def light(sid, data):
    print('que paso')
    print(data)





if __name__ == '__main__':
    if sio.async_mode == 'threading':
        # deploy with Werkzeug
        app.run(threaded=True)
    elif sio.async_mode == 'eventlet':
        # deploy with eventlet
        import eventlet
        import eventlet.wsgi
        eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    elif sio.async_mode == 'gevent':
        # deploy with gevent
        from gevent import pywsgi
        try:
            from geventwebsocket.handler import WebSocketHandler
            websocket = True
        except ImportError:
            websocket = False
        if websocket:
            pywsgi.WSGIServer(('', 5000), app,
                              handler_class=WebSocketHandler).serve_forever()
        else:
            pywsgi.WSGIServer(('', 5000), app).serve_forever()
    elif sio.async_mode == 'gevent_uwsgi':
        print('Start the application through the uwsgi server. Example:')
        print('uwsgi --http :5000 --gevent 1000 --http-websockets --master '
              '--wsgi-file app.py --callable app')
    else:
       print('Unknown async_mode: ' + sio.async_mode)
