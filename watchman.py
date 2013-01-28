import pyinotify
import tornado

from tornado.wsgi import WSGIContainer

from sockjs.tornado import SockJSRouter, SockJSConnection

from pusher import EchoConnection 
from webapp import interface
import json
import time
from Queue import Queue

ioloop = tornado.ioloop.IOLoop.instance()

eventq = Queue()


# Inotify handler
def handle_read_callback(notifier):
    eventq.put("EVENT!")


if __name__ == '__main__':
    
    # start the websocket (sockJS) server
    EchoRouter = SockJSRouter(EchoConnection, '/echo')
    app = tornado.web.Application(EchoRouter.urls)
    app.listen(9999)
 
    # start the webapp 
    container = WSGIContainer(interface)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(8888)    

    
    # Inotify setup
    wm = pyinotify.WatchManager()
    notifier = pyinotify.TornadoAsyncNotifier(wm, ioloop, callback=handle_read_callback)
    wm.add_watch('/home/bfer/tmp/sandbox', pyinotify.IN_CREATE|pyinotify.IN_DELETE|pyinotify.IN_MODIFY)


    # we add a ticker for testing
    def tick():
      EchoConnection.dispatch_all(json.dumps({'time':time.time()}))
    pc = tornado.ioloop.PeriodicCallback(tick, 1000)
    pc.start()
    
    # clears the queue and sends messages to clients every iteration
    def clearqueue():
      while not eventq.empty():
        try:
          EchoConnection.dispatch_all(eventq.get(False))
        except Queue.Empty:
          pass
      tornado.ioloop.IOLoop.instance().add_callback(clearqueue)
    clearqueue()

    # Get the show on the road!
    ioloop.start()

# Because I'm a pedant
ioloop.close()
notifier.stop()
