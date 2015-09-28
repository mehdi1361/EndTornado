__author__ = 'mousavi'
__author__ = 'mousavi'

import urllib2, sys, time, random

for i in range(100000):
    a = time.time()
    sys.stdout.write("connection number: %s \r" % i)
    mobile = random.randint(1111111, 9999999)
    transid = random.randint(11111, 99999)
    # u = urllib2.urlopen('http://cp.mobinone.org:36001/mmp/service/delivery?subscriber=921%s&Id=%s&status=1&shortcode=234' % (mobile, transid))
    u = urllib2.urlopen(
        'http://192.168.0.125:2051/api?subscriber=921%s&Id=%s&status=1&shortcode=234' % (mobile, transid))
    sys.stdout.write("process time: %s \r" % (time.time() - a))
    if u.code != 200:
        print "not right!"
    print "process time: %s and  mobileno:%s" % (time.time() - a, mobile)
    # sys.stdout.write("response code: %s \r"%u.code)
    sys.stdout.flush()

