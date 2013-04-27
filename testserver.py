import sys

from twisted.internet import reactor, task
from twisted.python import log

from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS

import simplejson as json
import random

class TestServerProtocol(WebSocketServerProtocol):
    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, msg, binary):
        print "Received message: %s" % msg
        print json.loads(msg)
        #self.factory.broadcast("'%s' from self.peerstr" % msg)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)

    def format_message(self, data):
        print data
        return json.dumps(data)

class TestServerFactory(WebSocketServerFactory):

    def __init__(self, url, debug = False, debugCodePaths = False):
        WebSocketServerFactory.__init__(self, url, debug=debug, debugCodePaths=debugCodePaths)
        self.clients = []
        self.positions = {}
        self.tickcount = 0
        self.tick()

    def tick(self):
        self.tickcount += 1
        #self.broadcast("tick %d" % self.tickcount)
        for client in self.clients:
            self.positions[client.peerstr] = {
                'x': self.positions.get(client.peerstr, {}).get('x', random.randint(-10,10)) + random.randint(-1,1),
                'y': self.positions.get(client.peerstr, {}).get('y', random.randint(-10,10)) + random.randint(-1,1),
            }
        self.broadcast(self.positions)
        reactor.callLater(0.1, self.tick)

    def register(self, client):
        if not client in self.clients:
            print "registered client " + client.peerstr
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print "unregistered client " + client.peerstr
            self.clients.remove(client)

    def broadcast(self, data):
        print "Broadcasting data: %s" % data
        for c in self.clients:
            message = c.format_message(data)
            c.sendMessage(message)
            print "message sent to %s" % c.peerstr

if __name__ == '__main__':
    log.startLogging(sys.stdout)

    factory = TestServerFactory("ws://0.0.0.0:9000", debug = False)
    factory.protocol = TestServerProtocol
    listenWS(factory)

    reactor.run()
