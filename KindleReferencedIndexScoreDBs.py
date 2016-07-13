import anydbm
import cPickle as pickle
import hashlib
from peewee import *
from datetime import datetime
import sys
import md5
import warnings

warnings.filterwarnings('ignore', 'Incorrect date value:*')

mydb = MySQLDatabase(
       database='kindle',
       user='root',
       password="1234",
       host="127.0.0.1",
       port=3306)

SEED_EXIST              = True
SEED_NO_EXIST           = False

class Serialized(Model):
    keyurl      = CharField(primary_key=True)
    date        = DateField(default=datetime.now() )
    serialized  = TextField()
    class Meta:
        database = mydb #
# create table
if not Serialized.table_exists():
    mydb.create_tables([Serialized], True)


# open db
def initiate_data(all_scraping_data):
    '''legacy
    db = anydbm.open('objects.db', 'c')
    for k, v in db.iteritems():
        loads = pickle.loads(v)
        all_scraping_data.append( (loads.normalized_url , loads) )
    if len(db.keys()) > 0 :
        res_mode = True
    else:
        res_mode = False
    db.close()
    '''
    for serialized in Serialized.select():
        print serialized.keyurl, serialized.date, pickle.loads(str(serialized.serialized))
        loads = pickle.loads( str(serialized.serialized) )
        all_scraping_data.append( (loads.normalized_url , loads) )
    if len(all_scraping_data) > 0:
        return SEED_EXIST
    return SEED_NO_EXIST

# close db
def finish_procedure(all_scraping_data):
    '''legacy
    db = anydbm.open('objects.db', 'c')
    for normalized_url, obj in all_scraping_data:
        dumps = pickle.dumps(obj)
        sha = hashlib.sha224(dumps).hexdigest()
        db[sha] = dumps
    db.close()
    '''
    for normalized_url, scraping_data in all_scraping_data:
        write_each(scraping_data)
# write each 
def write_each(scraping_data):
    '''legacy
    db = anydbm.open('objects.db', 'c')
    dumps = pickle.dumps(scraping_data)
    sha = hashlib.sha224(dumps).hexdigest()
    db[sha] = dumps
    db.close()
    '''
    '''
    文字列のエンコーディングに失敗した場合、書き込みを行わず、パスする
    '''
    dumps  = pickle.dumps(scraping_data)
    try:
        keyurl = str( hashlib.sha224(scraping_data.url).hexdigest() )
    except:
        return
    query = Serialized.select().where(Serialized.keyurl == keyurl)
    '''
    MySQLだから例外をよく吐く
    '''
    if not query.exists():
        Serialized.create(keyurl=keyurl,
           date=datetime.utcnow(),
           serialized=dumps
           )
    else:
        q = Serialized.update(
           date=datetime.utcnow(),
           serialized=dumps
           ).where( Serialized.keyurl==keyurl )
        q.execute()

    
