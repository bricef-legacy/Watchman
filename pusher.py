

from tornado import web, ioloop
from sockjs.tornado import SockJSRouter, SockJSConnection



#
# SockJs handler
#
class EchoConnection(SockJSConnection):
  clients = set()

  def on_open(self, info):
    # When new client comes in, will add it to the clients list
    self.clients.add(self)

  def on_message(self, msg):
    # For every incoming message, broadcast it to all clients
    self.broadcast(self.clients, msg)

  def on_close(self):
    # If client disconnects, remove him from the clients list
    self.clients.remove(self)

  @classmethod
  def dump_stats(cls):
    # Print current client count
    print 'Clients: %d' % (len(cls.clients))
 
  @classmethod
  def dispatch_all(cls, data):
    for client in cls.clients:
      client.send(data)
  

