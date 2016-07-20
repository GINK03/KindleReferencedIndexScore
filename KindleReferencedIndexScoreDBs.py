# coding: utf-8
from __future__ import print_function
import anydbm
import cPickle as pickle
import hashlib
from peewee import *
from datetime import datetime
import sys
import md5
import warnings
import time

warnings.filterwarnings('ignore', 'Incorrect date value:*')

mydb = MySQLDatabase(
       database = 'kindle',
       user     = 'root',
       password = '1234',
       host     = '127.0.0.1',
       port     = 3306)

SEED_EXIST              = True
SEED_NO_EXIST           = False
RETRY_NUM               = 10
DELAY                   = 1.0
CTL_DELIM               = ''

class Serialized(Model):
    keyurl              = CharField(primary_key=True)
    date                = DateTimeField(default=datetime.now() )
    serialized          = TextField()
    datetime_reviews    = DateTimeField(default=None )
    serialized_reviews  = TextField()
    serialized_asins    = TextField()
    class Meta:
        database = mydb 

"""
serialized$B%F!<%V%k$,B8:_$7$J$1$l$P?75,:n@.(B
"""
if not Serialized.table_exists():
    mydb.connect()
    mydb.create_tables([Serialized], True)
    mydb.close()

"""
MySQL$B$N%G!<%?$rA4It0z$-$@$9$,!"CY$$(B
"""
def initiate_data(all_scraping_data):
    for serialized in Serialized.select():
        """
        NOTE: $B2u$l$?%(%s%H%j$OL5;k$7$FFI$_9~$^$J$$(B
        """
        try:
            print(serialized.keyurl, serialized.date, pickle.loads(str(serialized.serialized)))
            scraping_data = pickle.loads(str(serialized.serialized) )
        except:
            print('[WARN] SQL data is broken.')
            serialized.delete()
            continue
        all_scraping_data.append((scraping_data.normalized_url , scraping_data) )
    if len(all_scraping_data) > 0:
        return SEED_EXIST
    return SEED_NO_EXIST

"""
$B%G!<%?$rA4<hF@$7$F%*%s%a%b%j$KJQ49$9$kI,MW$,$J$$>l9g$d!";2>H(BIF$B$r;H$$$?$/$J$$>l9g$KMxMQ$9$k(B
"""
def initiate_data_generator():
    for serialized in Serialized.select().iterator():
        key             = serialized.keyurl
        scraping_data   = pickle.loads(str(serialized.serialized) )
        yield (key, scraping_data, serialized.serialized.replace('\n', CTL_DELIM) )

"""
limit$BIU$-(Bgenerator
$BB?$9$.$k>pJs$r@)8B$9$k(B
"""
def initiate_data_limit_generator(num):
    for serialized in Serialized.select().limit(num).iterator():
        key             = serialized.keyurl
        scraping_data   = pickle.loads( str(serialized.serialized) )
        yield (key, scraping_data, serialized.serialized.replace('\n', CTL_DELIM) )

"""
scraping_data$B%$%s%9%?%s%9$,L$EPO?$N:]!"0l3gEPO?$9$k(B
"""
def finish_procedure(all_scraping_data):
    for normalized_url, scraping_data in all_scraping_data:
        write_each(scraping_data)

"""
scraping_data$B%$%s%9%?%s%9$rC`<!EPO?$9$k(B
multi process$B%"%/%;%9$N:]$G$bF0$/$h$&$K(Bsql$B%3%M%/%7%g%s%$%s%9%?%s%9$r:n$j$J$7$F$$$k(B
"""
def write_each(scraping_data):
    """
    $B%5%V%W%m%;%9$H$7$F5/F0$7$?8e$O!"%3%M%/%7%g%s$N;H$$$^$o$7$,$G$-$J$/$J$k$N$G!"%3%M%/%7%g%s$rGK4~$7!":n$jD>$9(B
    """
    try:
        mydb.close()
    except:
        print('[WARN] Mysql conn is already closed!')
    try:
        _db = MySQLDatabase(
            database = 'kindle',
            user     = 'root',
            password = '1234',
            host     = '127.0.0.1',
            port     = 3306)
        _db.connect()
    except:
        print('[CRIT] Cannot creal MySQL connector!', write_each.__name__)
        return 

    dumps                   = pickle.dumps(scraping_data)
    serialized_reviews      = pickle.dumps(scraping_data.reviews)
    reviews_datetime        = scraping_data.reviews_datetime
    serialized_asins        = pickle.dumps(scraping_data.asins)
    """
    $BJ8;zNs$N%(%s%3!<%G%#%s%0$K<:GT$7$?>l9g!"=q$-9~$_$r9T$o$:!"%Q%9$9$k(B
    #keyurl$B$O(BURL$B%Q%i%a!<%?$N$"$k$J$7$GL58B$KA}?#$7$&$k$+$iI,$:(Bnormalized_url$B$rMQ$$$k(B
    2016.7 ASIN$B$r(Bkeyurl$B$K@_Dj$9$k$h$&$K;EMM$rJQ99(B
    """
    # keyurl = str(hashlib.sha224(scraping_data.normalized_url.encode('utf-8') ).hexdigest() )
    keyurl                  = scraping_data.asin 

    try:
        pass
    except:
        _db.close()
        return
    is_query_exist = None
    for _ in range(RETRY_NUM):
        try:
            query = Serialized.select().where(Serialized.keyurl == keyurl)
            is_query_exist = query.exists()
            break
        except:
            print('[CRIT] cannot print query to MySQL or excute SQL query', write_each.__name__)
            time.sleep(1)
    """
    $B:G=i$N%/%(%jH/9T$K<:GT$7$?$i!"$"$-$i$a$F!"=q$-9~$_$7$J$$(B
    """
    if is_query_exist == None:
        _db.close()
        return
    """
    MySQL$B$@$+$iNc30$r$h$/EG$/(B
    TODO: except$B$N%$%s%9%?%s%9$r%-%c%C%A$9$k(B
    """
    for _ in range(RETRY_NUM):
        if not is_query_exist:
            try:
                Serialized.create(
                    keyurl              = keyurl,
                    date                = datetime.utcnow(),
                    serialized          = dumps,
                    datetime_reviews    = reviews_datetime,
                    serialized_reviews  = serialized_reviews,
                    serialized_asins    = serialized_asins
                )
                print('[DEBUG] crete a record to mysql', write_each.__name__, scraping_data.asin, scraping_data.title, scraping_data.url, Serialized)
                break
            except :
                print('[CRIT] cannot create new entry! try 10 times...',write_each.__name__, _)
                time.sleep(DELAY)
                continue
        else:
            """
            update$B$9$k:]$K$O!"%G!<%?NL$,>e2s$C$F$$$k>l9g$K$OJ]B8$;$:$K!"8E$$%G!<%?$r;H$$$^$o$9(B
            NOTE: len(scraping_data.html)  > len(scraping_data.html)$B$J$i$P%"%C%W%G!<%H(B
            NOTE: len(asins)            > len(old_asins)$B$J$i$P%"%C%W%G!<%H(B
            NOTE: len(reviews)          > len(old_reviews)$B$J$i$P%"%C%W%G!<%H(B
            """
            old_instance        = Serialized.get( Serialized.keyurl==keyurl )
            old_scraping_data   = pickle.loads( str(old_instance.serialized) )
            
            scraping_data.html              = (lambda x:x.html if len(x.html) > len(old_scraping_data.html) else old_scraping_data.html )(scraping_data)
            scraping_data.asins             = (lambda x:x.asins if len(x.asins) > len(old_scraping_data.asins) else old_scraping_data.asins )(scraping_data)
            scraping_data.reviews           = (lambda x:x.reviews if len(x.reviews) > len(old_scraping_data.reviews) else old_scraping_data.reviews )(scraping_data)
            scraping_data.reviews_datetime  = (lambda x:x.reviews_datetime if x.reviews_datetime > old_scraping_data.reviews_datetime else old_scraping_data.reviews_datetime )(scraping_data)

            try:
                q = Serialized.update(
                    date                = datetime.utcnow(),
                    serialized          = pickle.dumps(scraping_data),
                    datetime_reviews    = scraping_data.reviews_datetime,
                    serialized_reviews  = pickle.dumps(scraping_data.reviews),
                    serialized_asins    = pickle.dumps(scraping_data.asins)
                ).where( Serialized.keyurl==keyurl )
                q.execute()
                print('[DEBUG] update a record to mysql',write_each.__name__, scraping_data.asin, scraping_data.title, scraping_data.url, Serialized)
                break
            except:
                print('[CRIT] cannot update entry! try 10 times...', write_each.__name__, _)
                time.sleep(DELAY)
                continue
    _db.close()
