# coding: utf-8
import bs4
import sys
import urllib2
import urllib
# defined parameters
KINDLE_URL = 'https://www.amazon.co.jp/Kindle-%E3%82%AD%E3%83%B3%E3%83%89%E3%83%AB-%E9%9B%BB%E5%AD%90%E6%9B%B8%E7%B1%8D/b/ref=topnav_storetab_kinc?ie=UTF8&node=2250738051'
print 'テスト'
sys.exit(0)
if __name__ == '__main__':
    html = urllib2.urlopen(KINDLE_URL).read()
    soup = bs4.BeautifulSoup(html)

    for a in soup.find_all('a'):
        if a.has_attr('href'):
            print urllib.unquote(a['href']), a['href'], a.string
    

