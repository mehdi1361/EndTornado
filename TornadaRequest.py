import datetime
import logging
import memcache
from tornado import websocket, web, ioloop
# from DatabaseOp import AddRequest
from DatabaseOp import  UpdateDelivery
import sys, time
LOG_FILENAME = 'Log/RequestLog.out'
logging.basicConfig(filename=LOG_FILENAME,
                            level=logging.DEBUG,
                            )

class Caching(object):
    def __init__(self, hostname="127.0.0.1", port="11211"):
        self.hostname = "%s:%s" % (hostname, port)
        self.server = memcache.Client([self.hostname])

    def set(self, key, value, expiry=900):
        self.server.set(key, value, expiry)

    def get(self, key):
        return self.server.get(key)

    def delete(self, key):
        self.server.delete(key)

class IndexHandler(web.RequestHandler):
    ''' index http normal handler'''
    def get(self):
        # self.render("index.html")
        print "service worked"


class ApiHandler(web.RequestHandler):
    @web.asynchronous
    def get(self, *args):
        aaa = time.time()
        self._data = {
            'transactionId': self.get_argument("Id"),
            'subscriber': self.get_argument("subscriber"),
            'status': self.get_argument("status"),
            'shortcode': self.get_argument("shortcode"),
        }
        logging.debug('This message should go to the log file')
        sys.stdout.write(str(time.time() - aaa)+"\n")
        sys.stdout.write(self.request.remote_ip)
        sys.stdout.write(" [%s] " % datetime.datetime.now())
        sys.stdout.write(self.request.uri)
        self.finish()

    def on_finish(self):
        checkcache = Caching()
        s = checkcache.get(str(self._data['transactionId']))
        if s is None:
            checkcache.set(str(self._data['transactionId']), self._data['subscriber'])
            UpdateDelivery.delay(**self._data)

app = web.Application([
    (r'/', IndexHandler),
    (r'/api', ApiHandler),
])

if __name__ == '__main__':
    app.listen(2051)
    ioloop.IOLoop.instance().start()
