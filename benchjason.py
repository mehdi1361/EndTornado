#!/usr/bin/python
import urllib,urllib2

# url = 'http://192.168.0.125:2051/api'
url = 'http://localhost/pyt/t.py'
parameters = '''[{"Id":"201647109","subscriber":"9156765887","status":"5","shortcode":"203815","part":"1"},{"Id":"72082023","subscriber":"9102178689","status":"4012","shortcode":"203813","part":"0"},{"Id":"143908513","subscriber":"9109085727","status":"4012","shortcode":"203813","part":"0"},{"Id":"43340435","subscriber":"9157661685","status":"4012","shortcode":"203813","part":"0"},{"Id":"143358147","subscriber":"9128360042","status":"12","shortcode":"203813","part":"0"},{"Id":"27048118","subscriber":"9122957030","status":"1","shortcode":"203813","part":"1"},{"Id":"72328665","subscriber":"9100571523","status":"4012","shortcode":"203813","part":"0"},{"Id":"65550430","subscriber":"9157158190","status":"4012","shortcode":"203813","part":"0"},{"Id":"176519019","subscriber":"9175430861","status":"4012","shortcode":"203813","part":"0"},{"Id":"76136359","subscriber":"9103379648","status":"4012","shortcode":"203813","part":"0"}]'''
#data = urllib.(parameters)    # Use urllib to encode the parameters
request = urllib2.Request(url, str(parameters))
response = urllib2.urlopen(request)    # This request is sent in HTTP POST
page = response.read(200000)