import sys

from twisted.internet import reactor, task
from twisted.python import log

from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS

class TestServerProtocol(WebSocketServerProtocol):
    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, msg, binary):
        print "sending echo:", msg
        self.factory.broadcast("'%s' from self.peerstr" % msg)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)

class TestServerFactory(WebSocketServerFactory):

    def __init__(self, url, debug = False, debugCodePaths = False):
        WebSocketServerFactory.__init__(self, url, debug=debug, debugCodePaths=debugCodePaths)
        self.clients = []
        self.tickcount = 0
        self.tick()

    def tick(self):
        self.tickcount += 1
        self.broadcast("tick %d" % self.tickcount)
        reactor.callLater(1, self.tick)

    def register(self, client):
        if not client in self.clients:
            print "registered client " + client.peerstr
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print "unregistered client " + client.peerstr
            self.clients.remove(client)

    def broadcast(self, msg):
        print "Broadcasting message: %s" % msg
        for c in self.clients:
            c.sendMessage(msg)
            print "message sent to %s" % c.peerstr

if __name__ == '__main__':
    log.startLogging(sys.stdout)

    factory = TestServerFactory("ws://0.0.0.0:9000", debug = False)
    factory.protocol = TestServerProtocol
    listenWS(factory)

    reactor.run()
