import anydbm
import cPickle as pickle
import hashlib

# open db
def initiate_data(all_scraping_data):
    res_mode = False
    db = anydbm.open('objects.db', 'c')
    for k, v in db.iteritems():
        try:
            loads = pickle.loads(v)
        except:
            continue
        all_scraping_data.append( (loads.normalized_url , loads) )
        #print loads.normalized_url, loads, map(lambda x:x.from_url, loads.evaluated)
    if len(db.keys()) > 0 :
        res_mode = True
    else:
        res_mode = False
    db.close()
    return res_mode

# close db
def finish_procedure(all_scraping_data):
    db = anydbm.open('objects.db', 'c')
    for normalized_url, obj in all_scraping_data:
        dumps = pickle.dumps(obj)
        sha = hashlib.sha224(dumps).hexdigest()
        db[sha] = dumps
    db.close()

# write each 
def write_each(scraping_data):
    db = anydbm.open('objects.db', 'c')
    dumps = pickle.dumps(scraping_data)
    sha = hashlib.sha224(dumps).hexdigest()
    db[sha] = dumps
    db.close()
