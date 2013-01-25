Ideas
=====

Use a [Tornado wsgi container](http://www.tornadoweb.org/documentation/wsgi.html) for the webapp and a [sockjs container](https://github.com/bricef/origin-prototype/blob/master/Server/proxy.py) for the socket connection. Can also use the [TornadoAsyncNotifier](https://github.com/seb-m/pyinotify/blob/master/python2/examples/tornado_notifier.py) for the filesystem watching. 


Communication between loops achieved using good ol' Python queues


Would look a little like:


```python

import pyinotify
from tornado.ioloop import IOLoop
from tornado import web
from tornado.wsgi import WSGIContainer
from sockjs.tornado import SockJSRouter, SockJSConnection

ioloop = IOLoop.instance()

#
# Inotify handler
#
def handle_read_callback(notifier):
    """
    Just stop receiving IO read events after the first
    iteration (unrealistic example).
    """
    print('handle_read callback')
    notifier.io_loop.stop()


#
# SockJs handler
#
class EchoConnection(SockJSConnection):
    def on_message(self, msg):
        self.send(msg)

#
# Web handler (real would use bottle)
#
def simple_app(environ, start_response):
    status = "200 OK"
    response_headers = [("Content-type", "text/plain")]
    start_response(status, response_headers)
    return ["Hello world!\n"]

if __name__ == '__main__':
    #
    # SockJs setup
    #
    EchoRouter = SockJSRouter(EchoConnection, '/echo')
    app = web.Application(EchoRouter.urls)
    app.listen(9999)

    #
    # Inotify setup
    #
    wm = pyinotify.WatchManager()
    notifier = pyinotify.TornadoAsyncNotifier(wm, ioloop, callback=handle_read_callback)
    wm.add_watch('/tmp', pyinotify.ALL_EVENTS)

    #
    # Web setup
    #
    container = tornado.wsgi.WSGIContainer(simple_app)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(8888)

    #
    # Get the show on the road!
    #
    ioloop.start()

#
# Because I'm a pedant
#
ioloop.close()
notifier.stop()
```
