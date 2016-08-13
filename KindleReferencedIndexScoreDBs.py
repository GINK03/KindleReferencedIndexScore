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
from KindleReferencedIndexScoreConfigMapper import *
warnings.filterwarnings('ignore', 'Incorrect date value:*')

mydb = MySQLDatabase(
       database = 'kindle',
       user     = 'root',
       password = '1234',
       host     = CM.SQL_IP,
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
        try:
            key             = serialized.keyurl
            scraping_data   = pickle.loads(str(serialized.serialized) )
            yield (key, scraping_data, serialized.serialized.replace('\n', CTL_DELIM) )
        except UnicodeEncodeError, e:
            print('[CRIT] Cannot decode as ASCII', e)
            continue

import MySQLdb.cursors
import plyvel
class MySQLWrapper:
  @staticmethod
  def get_all_data_iter_raw():
    connection = MySQLdb.connect(
        host   = CM.SQL_IP,
        user   = "root",
        passwd = "1234",
        db     = "kindle",
        cursorclass = MySQLdb.cursors.SSCursor)
    cursor = connection.cursor()
    cursor.execute('SELECT keyurl, serialized FROM serialized')
    result = cursor.fetchone()
    while result != None:
      keyurl, raw_scraping_data = result[0], result[1]
      yield (keyurl, raw_scraping_data)
      result = cursor.fetchone()

  @staticmethod 
  def dump2leveldb(filepath):
    print('[INFO] Start dump2leveldb to ', filepath)
    db = plyvel.DB('./' + filepath, create_if_missing=True)
    for keyurl, raw_scraping_data in MySQLWrapper.get_all_data_iter_raw():
      if db.get(keyurl) == None:
        db.put(keyurl, raw_scraping_data)
    db.close()
    print('[INFO] Finish dump2leveldb.')
  
  @staticmethod
  def get_all_rand_iter():
    connection = MySQLdb.connect(
        host   = CM.SQL_IP,
        user   = "root",
        passwd = "1234",
        db     = "kindle",
        cursorclass = MySQLdb.cursors.SSCursor)
    cursor = connection.cursor()
    cursor.execute('SELECT keyurl, serialized FROM serialized order by RAND()')
    while True:
      result = cursor.fetchone()
      if not result:
        break
      keyurl, scraping_data = result[0], pickle.loads(result[1])
      yield (keyurl, scraping_data)

"""
$B%5!<%P%5%$%I%$%F%l!<%?$J$N$G!"%a%b%j$N>CHqNL$rM^$($k$3$H$,2DG=(B
"""
def get_all_data_iter():
    connection = MySQLdb.connect(
        host   = CM.SQL_IP,
        user   = "root",
        passwd = "1234",
        db     = "kindle",
        cursorclass = MySQLdb.cursors.SSCursor)

    cursor = connection.cursor()
    cursor.execute('SELECT keyurl, serialized FROM serialized')
    result = cursor.fetchone()
    while result != None:
      keyurl, scraping_data = result[0], pickle.loads(result[1])
      yield (keyurl, scraping_data)
      result = cursor.fetchone()


def get_all_data_iter_box(box_size = CM.DESIRABLE_PROCESS_NUM):
    connection = MySQLdb.connect(
        host   = CM.SQL_IP,
        user   = "root",
        passwd = "1234",
        db     = "kindle",
        cursorclass = MySQLdb.cursors.SSCursor)
    cursor = connection.cursor()
    cursor.execute('SELECT keyurl, serialized FROM serialized')
    result = cursor.fetchone()
    while result != None:
      keyurl, scraping_data = result[0], pickle.loads(result[1])
      try:
        results = [ cursor.fetchone() for _ in range(box_size)]
      except OperationalError, e:
        """
        $BNc30$,H/@8$7$?>l9g$O(Byield$B$r=*N;(B
        """
        break
      res_results = map(lambda x: (x[0], pickle.loads(x[1]) ), results) 
      if all(map(lambda x:x[0], res_results) ) == False:
        break
      yield res_results
"""
limit$BIU$-(Bgenerator
$BB?$9$.$k>pJs$r@)8B$9$k(B
"""
def initiate_data_limit_generator(num):
    for serialized in Serialized.select().limit(num).iterator():
        key             = serialized.keyurl
        try:
            scraping_data   = pickle.loads( str(serialized.serialized) )
            yield (key, scraping_data )
        except:
            continue


"""
scraping_data$B%$%s%9%?%s%9$,L$EPO?$N:]!"0l3gEPO?$9$k(B
"""
def finish_procedure(all_scraping_data):
    for normalized_url, scraping_data in all_scraping_data:
        write_each(scraping_data)

import time
from KindleReferencedIndexScoreClass import *
class SerializedUtils:

  """
  is_already_query_exist_and_too_old?
  retval: True, already query exists
          False, query not exists
  """
  @staticmethod
  def is_too_old_query(scraping_data):
      """
      $B%5%V%W%m%;%9$H$7$F5/F0$7$?8e$O!"%3%M%/%7%g%s$N;H$$$^$o$7$,$G$-$J$/$J$k$N$G!"%3%M%/%7%g%s$rGK4~$7!":n$jD>$9(B
      """
      try:
          mydb.close()
      except:
         # print('[WARN] Mysql conn is already closed!')
          pass
      try:
          _db = MySQLDatabase(
              database = 'kindle',
              user     = 'root',
              password = '1234',
              host     = CM.SQL_IP,
              port     = 3306)
          _db.connect()
      except:
          print('[CRIT] Cannot creal MySQL connector!', is_too_old_query.__name__)
          return False
      
      keyurl                  = scraping_data.asin 
      q = Serialized.select().where(Serialized.keyurl == keyurl)
      if not q.exists():
        print('[INFO] This access is first, it will create new record.' )
        return False
      serialized_raw = pickle.loads( str(Serialized.select().where(Serialized.keyurl == keyurl).get().serialized) )
      
      ScrapingDataHelp.attribute_valid(serialized_raw)
      old_time_stamp = serialized_raw.last_scrape_time
      print('[notice]', old_time_stamp)
      if time.time() - old_time_stamp < 86400 * 31:
        import hashlib
        print('[INFO]', serialized_raw.asin, ' is not too old, no need to scrape. ', ' md5', str(hashlib.md5(serialized_raw.html).hexdigest()))
        return True
      else:
        print('[INFO] {} is too old, re-scrape it.'.format(serialized_raw.asin) )
        return False
"""
is_already_analyzed?
NOTE: query$B$rH/9T$7$F!"(BScrapingData$B%$%s%9%?%s%9$N(Ball_tf != [] $B$G$J$1$l$P!"I>2A:Q$_$H$$$&$3$H$G(BTrue$B$rJV$9(B
NOTE: $B>e5-0J30$O(BFalse$B$rJV$9(B
"""
def is_already_analyzed(scraping_data):
    keyurl      = scraping_data.asin
    try:
        instance    = pickle.loads(str(Serialized.get(Serialized.keyurl == keyurl).serialized) )
    except UnicodeEncodeError, e:
        print('[CRIT] Cannot Encode pickle... give up data', e)
        return False
    except OperationalError, e:
        print('[CRIT] Peewee cannot operate MySQL... give up data', e)
        return False
    if hasattr(instance, 'all_tf') and instance.all_tf != []:
        return True
    else :
        return False

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
            host     = CM.SQL_IP,
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
    ASIN$B$r(Bkeyurl$B$K@_Dj$9$k$h$&$K;EMM$rJQ99(B
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
            #time.sleep(1)
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
                    serialized          = str(dumps).decode('utf-8'),
                    datetime_reviews    = reviews_datetime,
                    serialized_reviews  = str(serialized_reviews),
                    serialized_asins    = str(serialized_asins)
                )
                print(','.join(map(lambda x:str(x).replace(',', ''), ['[DEBUG] Created a record to mysql', write_each.__name__, scraping_data.asin, scraping_data.uniq_hash, scraping_data.title.encode('utf-8'), scraping_data.url.encode('utf-8'), scraping_data.harmonic_mean, scraping_data.relevancy, scraping_data.cooccurrence, scraping_data.normal_mean, Serialized]) ) )
                break
            except UnicodeDecodeError, e:
                print('[CRIT] Cannot create new entry! UnicodeDecodeError...', write_each.__name__, _, e)
                continue
            except IntegrityError, e:
                print('[CRIT] Cannot create new entry! because, itegrity error', write_each.__name__, _, e)
                break
            except OperationalError, e:
                print('[CRIT] cannot create new entry! OperationalErro r', e, write_each.__name__, _)
                break
        else:
            """
            1. update$B$9$k:]$K$O!"%G!<%?NL$,>e2s$C$F$$$k>l9g$K$OJ]B8$;$:$K!"8E$$%G!<%?$r;H$$$^$o$9(B
            NOTE: len(scraping_data.html)  > len(scraping_data.html)$B$J$i$P%"%C%W%G!<%H(B
            NOTE: len(asins)            > len(old_asins)$B$J$i$P%"%C%W%G!<%H(B
            NOTE: len(reviews)          > len(old_reviews)$B$J$i$P%"%C%W%G!<%H(B
            NOTE: $B?7$7$$%"%H%j%S%e!<%H$NA}2C$O!"MWAG$NI>2A@h%*%V%8%'%/%H$K?7$7$$$b$N$r;H$&$H$$$&86B'$r<i$l$P!"(B
                $B!!%"%H%j%S%e!<%H<+BN$,>C5n$5$l$k$H$$$&$3$H$O$J$$(B
            2. Evaluator$B$,<B9T:Q$_$N>l9g!"%"%C%W%G!<%H$7$J$$(B
            3. html$B$,B8:_$7$J$$>l9g!"(Bhtml$B>pJsNL$,B?$$$[$&$r;D$9(B
            """
            old_instance        = Serialized.get( Serialized.keyurl==keyurl )
            try:
                old_scraping_data   = pickle.loads( str(old_instance.serialized) )
            except UnicodeEncodeError, e:
                print('[CRIT] Cannot load pickled data', e, old_instance.keyurl)
                break

            """ 1 """ 
            scraping_data.asins             = (lambda x:x.asins if len(x.asins) > len(old_scraping_data.asins) else old_scraping_data.asins )(scraping_data)
            scraping_data.reviews           = (lambda x:x.reviews if len(x.reviews) > len(old_scraping_data.reviews) else old_scraping_data.reviews )(scraping_data)
            scraping_data.reviews_datetime  = (lambda x:x.reviews_datetime if x.reviews_datetime > old_scraping_data.reviews_datetime else old_scraping_data.reviews_datetime )(scraping_data)
            scraping_data.cooccurrence      = (lambda x:x.cooccurrence if x.cooccurrence > 0 else old_scraping_data.cooccurrence )(scraping_data)

            """ 2. """
            if hasattr(old_instance, 'harmonic_mean') and hasattr(old_instance, 'normal_mean') and \
                (old_instance.harmonic_mean != 0. or old_instance.normal_mean != 0 or \
                old_instance.product_info != '' or \
                old_instance.product_tf != [] or \
                old_instance.reviews    != [] or \
                old_instance.reviews_tf != [] ) :
                    #break
                    pass

            """ 3. """
            if old_scraping_data.html == None:
                old_scraping_data.html = ''
            if scraping_data.html != None: 
                scraping_data.html              = (lambda x:x.html if len(x.html) > len(old_scraping_data.html) else old_scraping_data.html )(scraping_data)

            try:
                q = Serialized.update(
                    date                = datetime.utcnow(),
                    serialized          = pickle.dumps(scraping_data),
                    datetime_reviews    = scraping_data.reviews_datetime,
                    serialized_reviews  = pickle.dumps(scraping_data.reviews),
                    serialized_asins    = pickle.dumps(scraping_data.asins)
                ).where( Serialized.keyurl==keyurl )
                q.execute()
                print(','.join(map(lambda x:str(x).replace(',', ''), ['[DEBUG] update a record to mysql', write_each.__name__, scraping_data.asin, scraping_data.title.encode('utf-8'), scraping_data.url.encode('utf-8'), scraping_data.harmonic_mean, scraping_data.relevancy, scraping_data.cooccurrence, scraping_data.normal_mean, ' '.join(scraping_data.relevancy_term), Serialized]) ) )
                break
            except UnicodeDecodeError, e:
                print('[CRIT] cannot update entry! try 10 times...', e, write_each.__name__, _)
                continue
            except OperationalError, e:
                print('[CRIT] cannot update entry! peewee OperationalError occurred...', e, write_each.__name__, _)
                break

    _db.close()
