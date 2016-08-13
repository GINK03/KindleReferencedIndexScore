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
serializedテーブルが存在しなければ新規作成
"""
if not Serialized.table_exists():
    mydb.connect()
    mydb.create_tables([Serialized], True)
    mydb.close()

"""
MySQLのデータを全部引きだすが、遅い
"""
def initiate_data(all_scraping_data):
    for serialized in Serialized.select():
        """
        NOTE: 壊れたエントリは無視して読み込まない
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
データを全取得してオンメモリに変換する必要がない場合や、参照IFを使いたくない場合に利用する
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
サーバサイドイテレータなので、メモリの消費量を抑えることが可能
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
        例外が発生した場合はyieldを終了
        """
        break
      res_results = map(lambda x: (x[0], pickle.loads(x[1]) ), results) 
      if all(map(lambda x:x[0], res_results) ) == False:
        break
      yield res_results
"""
limit付きgenerator
多すぎる情報を制限する
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
scraping_dataインスタンスが未登録の際、一括登録する
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
      サブプロセスとして起動した後は、コネクションの使いまわしができなくなるので、コネクションを破棄し、作り直す
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
NOTE: queryを発行して、ScrapingDataインスタンスのall_tf != [] でなければ、評価済みということでTrueを返す
NOTE: 上記以外はFalseを返す
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
scraping_dataインスタンスを逐次登録する
multi processアクセスの際でも動くようにsqlコネクションインスタンスを作りなしている
"""
def write_each(scraping_data):
    """
    サブプロセスとして起動した後は、コネクションの使いまわしができなくなるので、コネクションを破棄し、作り直す
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
    文字列のエンコーディングに失敗した場合、書き込みを行わず、パスする
    #keyurlはURLパラメータのあるなしで無限に増殖しうるから必ずnormalized_urlを用いる
    ASINをkeyurlに設定するように仕様を変更
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
    最初のクエリ発行に失敗したら、あきらめて、書き込みしない
    """
    if is_query_exist == None:
        _db.close()
        return
    """
    MySQLだから例外をよく吐く
    TODO: exceptのインスタンスをキャッチする
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
            1. updateする際には、データ量が上回っている場合には保存せずに、古いデータを使いまわす
            NOTE: len(scraping_data.html)  > len(scraping_data.html)ならばアップデート
            NOTE: len(asins)            > len(old_asins)ならばアップデート
            NOTE: len(reviews)          > len(old_reviews)ならばアップデート
            NOTE: 新しいアトリビュートの増加は、要素の評価先オブジェクトに新しいものを使うという原則を守れば、
                　アトリビュート自体が消去されるということはない
            2. Evaluatorが実行済みの場合、アップデートしない
            3. htmlが存在しない場合、html情報量が多いほうを残す
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
