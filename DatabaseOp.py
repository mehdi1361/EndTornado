from celery import Celery
import MySQLdb
import datetime
import memcache
from db_op import DB
import json
app = Celery('tasks', broker='amqp://guest@localhost//')

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

@app.task
def UpdateDelivery(transactionId, subscriber, status, shortcode):
    db = MySQLdb.connect("localhost", "meh.mous", "5tgbNHY^", "mmp" )
    cursor = db.cursor()
    result = cursor.execute('''UPDATE outbound
                      SET status = %s, description = %s, updated_at = %s
                      WHERE (transactionid = %s)''', (Delivery(status), FindDescription(status), datetime.datetime.now(),transactionId))
    WriteToFile.delay(transactionId, result)
    db.commit()
    db.close()


@app.task
def update_delivery_json(json_string):
    db = DB()
    list_delivery = json.loads(json_string)
    for data in list_delivery:
        checkcache = Caching()
        s = checkcache.get(str(data['Id']))
        if s is None:
            checkcache.set(str(data['Id']), data['subscriber'])
            cursor = db.query('''UPDATE outbound
                      SET status = %s, description = %s, updated_at = %s
                      WHERE (transactionid = %s)''', (Delivery(data['status']), FindDescription(data['status']), datetime.datetime.now(),data['Id']))
            WriteToFile.delay(data['Id'], cursor)

@app.task
def WriteToFile(TransactionId,Result):
    print "Hello"
    f = open('Log/myfile.out','a')
    f.write('update DataBase with transactionId: %s Successfull:{%s} at :%s\n' % (TransactionId, Result, datetime.datetime.now()))
    f.close()


def Delivery(x):
    return {
      '1': 'delivered',
      1: 'delivered',
      '2': 'failed',
      2: 'failed',
      '3': 'failed',
      3: 'failed',
      '4': 'failed',
      4: 'failed',
      5: 'failed',
      '5': 'failed',
      '6': 'error Status',
      6: 'error Status',
    }.get(x, 'ocs')

def FindDescription(x):
     return {
        '1': 'Message Reported As Delivered',
        1: 'Message Reported As Delivered',
        '2': 'Message Reported As Failed With Error Code: %s' % x,
        2: 'Message Reported As Failed With Error Code: %s' % x,
        '3': 'Message Reported As Failed With Error Code: %s' % x,
        3: 'Message Reported As Failed With Error Code: %s' % x,
        '4': 'Message Reported As Failed With Error Code: %s' % x,
        4: 'Message Reported As Failed With Error Code: %s' % x,
        '5': 'Message Reported As Failed With Error Code: %s' % x,
        5: 'Message Reported As Failed With Error Code: %s' % x,
        '6': 'error Status',
        6: 'error Status',
    } .get(x, 'Message Reported As OCS With Error Code: %s' % x)