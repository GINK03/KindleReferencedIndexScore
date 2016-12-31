# coding: utf-8
import urllib
import urllib2

txt = "全力"

q = urllib2.quote(txt)
print q

print urllib2.unquote("%E9%9B%BB")


