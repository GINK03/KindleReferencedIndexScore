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
       database='kindle',
       user='root',
       password="1234",
       host="127.0.0.1",
       port=3306)

SEED_EXIST              = True
SEED_NO_EXIST           = False
RETRY_NUM               = 10
DELAY                   = 1.0

class Serialized(Model):
    keyurl      = CharField(primary_key=True)
    date        = DateField(default=datetime.now() )
    serialized  = TextField()
    class Meta:
        database = mydb #

# create table
if not Serialized.table_exists():
    mydb.connect()
    mydb.create_tables([Serialized], True)
    mydb.close()

# open db
def initiate_data(all_scraping_data):
    for serialized in Serialized.select():
        """
        $B2u$l$?%(%s%H%j$OL5;k$7$FFI$_9~$^$J$$(B
        TODO: $B2u$l$?%(%s%H%j$r:o=|$9$k(B
        """
        try:
            print serialized.keyurl, serialized.date, pickle.loads(str(serialized.serialized))
            scraping_data = pickle.loads( str(serialized.serialized) )
        except:
            print '[SQL_DATA_BROKEN]'
            serialized.delete()
            continue
        all_scraping_data.append( (scraping_data.normalized_url , loads) )
    if len(all_scraping_data) > 0:
        return SEED_EXIST
    return SEED_NO_EXIST

"""
$B%G!<%?$rA4<hF@$7$F%*%s%a%b%j$KJQ49$9$kI,MW$,$J$$>l9g$d!";2>H(BIF$B$r;H$$$?$/$J$$>l9g$KMxMQ$9$k(B
"""
def initiate_data_generator():
    for serialized in Serialized.select():
        key             = serialized.keyurl
        scraping_data   = pickle.loads( str(serialized.serialized) )
        yield (key, scraping_data)


# close db
def finish_procedure(all_scraping_data):
    for normalized_url, scraping_data in all_scraping_data:
        write_each(scraping_data)
# write each 
def write_each(scraping_data):
    '''
    $B%5%V%W%m%;%9$H$7$F5/F0$7$?8e$O!"%3%M%/%7%g%s$N;H$$$^$o$7$,$G$-$J$/$J$k$N$G!"%3%M%/%7%g%s$rGK4~$7!":n$jD>$9(B
    '''
    try:
        mydb.close()
    except:
        print '[warnings] mysql conn is already closed!'
    _db = MySQLDatabase(
       database='kindle',
       user='root',
       password="1234",
       host="127.0.0.1",
       port=3306)
    _db.connect()
    '''
    $BJ8;zNs$N%(%s%3!<%G%#%s%0$K<:GT$7$?>l9g!"=q$-9~$_$r9T$o$:!"%Q%9$9$k(B
    '''
    dumps  = pickle.dumps(scraping_data)
    try:
        keyurl = str( hashlib.sha224(scraping_data.url).hexdigest() )
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
            print '[1] unko'
            time.sleep(1)
            continue
    '''
    $B:G=i$N%/%(%jH/9T$K<:GT$7$?$i!"$"$-$i$a$F!"=q$-9~$_$7$J$$(B
    '''
    if is_query_exist == None:
        _db.close()
        return
    '''
    MySQL$B$@$+$iNc30$r$h$/EG$/(B
    '''
    for _ in range(RETRY_NUM):
        if not is_query_exist:
            try:
                Serialized.create(keyurl=keyurl,
                    date=datetime.utcnow(),
                    serialized=dumps
                )
                break
            except:
                print '[]'
                time.sleep(DELAY)
                continue
        else:
            try:
                q = Serialized.update(
                    date=datetime.utcnow(),
                    serialized=dumps
                ).where( Serialized.keyurl==keyurl )
                q.execute()
                break
            except:
                print '[]'
                time.sleep(DELAY)
                continue
    print '[debug] write to mysql', Serialized
    _db.close()
