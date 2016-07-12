import anydbm
import cPickle as pickle
import hashlib
from peewee import *
from datetime import datetime
import sys
import md5

mydb = MySQLDatabase(
       database='kindle',
       user='root',
       password="1234",
       host="127.0.0.1",
       port=3306)

class Serialized(Model):
    keyurl      = CharField(primary_key=True)
    date        = DateField(default=datetime.now() )
    serialized  = TextField()
    class Meta:
        database = mydb #
# create table
if not Serialized.table_exists():
    mydb.create_tables([Serialized], True)

mydb.close()

# open db
def initiate_data(all_scraping_data):
    res_mode = False
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
        print serialized.keyurl, serialized.date, serialized.serialized
    #sys.exit(0)
    return res_mode

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
# write each 
def write_each(scraping_data):
    '''legacy
    db = anydbm.open('objects.db', 'c')
    dumps = pickle.dumps(scraping_data)
    sha = hashlib.sha224(dumps).hexdigest()
    db[sha] = dumps
    db.close()
    '''
    dumps  = pickle.dumps(scraping_data)
    keyurl = str( md5.new(scraping_data.url).hexdigest() )
    print keyurl
    query = Serialized.select().where(Serialized.keyurl == keyurl)
    if not query.exists():
        Serialized.create(keyurl=keyurl,
               date=datetime.utcnow(),
               serialized=dumps
               )
    else:
        q = Serialized.update(keyurl=keyurl,
               date=datetime.utcnow(),
               serialized=dumps
               )
        q.execute()
        q.close()
    query.close()

    
