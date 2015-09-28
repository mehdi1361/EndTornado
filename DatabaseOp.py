from celery import Celery
import MySQLdb
import datetime
app = Celery('tasks', broker='amqp://guest@localhost//')

@app.task
def UpdateDelivery(transactionId, subscriber, status, shortcode):
    db = MySQLdb.connect("localhost", "meh.mous", "5tgbNHY^", "mmp" )
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    result= cursor.execute('''UPDATE outbound
                      SET status = %s, description = %s, updated_at = %s
                      WHERE (transactionid = %s)''', (Delivery(status), FindDescription(status), datetime.datetime.now(),transactionId))
    WriteToFile.delay(transactionId, result)
    db.commit()
    db.close()

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