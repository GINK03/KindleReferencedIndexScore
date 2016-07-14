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
    class Meta:
        database = mydb 

"""
テーブルが存在しなければ新規作成
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
            print('[WARN]SQL data is broken.')
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
        key             = serialized.keyurl
        scraping_data   = pickle.loads( str(serialized.serialized) )
        yield (key, scraping_data, serialized.serialized.replace('\n', CTL_DELIM) )

"""
limit付きgenerator
多すぎる情報を制限する
"""
def initiate_data_limit_generator(num):
    for serialized in Serialized.select().limit(num).iterator():
        key             = serialized.keyurl
        scraping_data   = pickle.loads( str(serialized.serialized) )
        yield (key, scraping_data, serialized.serialized.replace('\n', CTL_DELIM) )

"""
scraping_dataインスタンスが未登録の際、一括登録する
"""
def finish_procedure(all_scraping_data):
    for normalized_url, scraping_data in all_scraping_data:
        write_each(scraping_data)

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
            host     = '127.0.0.1',
            port     = 3306)
        _db.connect()
    except:
        print('[CRIT] Cannot creal MySQL connector!')
        return 

    dumps                   = pickle.dumps(scraping_data)
    serialized_reviews      = pickle.dumps(scraping_data.reviews)
    reviews_datetime        = scraping_data.reviews_datetime
    """
    文字列のエンコーディングに失敗した場合、書き込みを行わず、パスする
    #keyurlはURLパラメータのあるなしで無限に増殖しうるから必ずnormalized_urlを用いる
    2016.7 ASINをkeyurlに設定するように仕様を変更
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
            print('[CRIT] cannot print query to MySQL or excute SQL query')
            time.sleep(1)
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
                    serialized          = dumps,
                    datetime_reviews    = reviews_datetime,
                    serialized_reviews  = serialized_reviews
                )
                break
            except :
                print('[CRIT] cannot create new entry! try 10 times...', _)
                time.sleep(DELAY)
                continue
        else:
            try:
                q = Serialized.update(
                    date                = datetime.utcnow(),
                    serialized          = dumps,
                    datetime_reviews    = reviews_datetime,
                    serialized_reviews  = serialized_reviews
                ).where( Serialized.keyurl==keyurl )
                q.execute()
                break
            except:
                print('[CRIT] cannot update entry! try 10 times...', _)
                time.sleep(DELAY)
                continue
    print('[DEBUG] write to mysql', scraping_data.asin, scraping_data.title, scraping_data.url, Serialized)
    _db.close()
