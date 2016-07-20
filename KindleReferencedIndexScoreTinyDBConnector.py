# coding: utf-8
from __future__ import print_function
from tinydb import TinyDB, Query
from collections import Counter
from KindleReferencedIndexScoreDBs import *

"""Database Design
データベースの今のところのデザイン
MySQLはデータベースの変更コストが高くて正直やってられない
{ 
asin:               string,
reviews:            list[string],
review_tf:          Counter,
product_info:       string,
product_info_tf:    Counter,
harmonic_mean:      float,
relavancy:          float,
is_good:            boolean,
is_bad:             boolean,
refarenced_asins:   list[string],
}
"""
class TBC:
    db = TinyDB('db.json')
    @staticmethod
    def merge_tinydb_from_mysql():
        for asinkey, scraping_data, _ in initiate_data_generator():

            converted = map(lambda x:(x.star, x.context, x.vote, x.hashes), \
                        scraping_data.reviews)
        
            obj = { 
                    'asin'          : asinkey,
                    'reviews'       : converted,
                    """
                    'review_tf'     : None,
                    'product_info'  : None,
                    'product_info_tf': None,
                    'harmonic_mean' : None,
                    'relavancy'     : None,
                    'is_good'       : None,
                    'is_bad'        : None
                    """
                    'refarenced_asins': scraping_data.asins
                    }
            Data = Query()
            res = TBC.db.search(Data.asin == asinkey )
            if res == [] or res == None:
                try:
                    TBC.db.insert(obj )
                except TypeError, e:
                    print('[CRIT] Error was occurred!', e)
            else:
                TBC.db.update(obj, Data.asin == asinkey )
                
    @staticmethod
    def merge_data(target_asin, obj):
        Data        = Query()
        target_obj  = TBC.db.search(Data.asin == target_asin )

    @staticmethod
    def save_tinydb(target_asin, obj):
        Data = Query()
        res = db.search(Data.asin == target_asin )
        if res == [] or res == None:
            try:
                TBC.db.insert(obj )
            except TypeError, e:
                print('[CRIT] Error was occurred!', e)
        else:
            TBC.db.update(obj, Data.asin == target_asin )

if __name__ == '__main__':
    """
    メイン文として呼び出されたときの処理：通常ありえないので、アドホックな処理
    """
    TBC.merge_tinydb_from_mysql()
