# coding: utf-8
from __future__ import print_function
import bs4
import plyvel
import sys
import urllib2
import urllib
import os
import argparse
import multiprocessing as mp
import threading
import datetime
import sys
import time
from KindleReferencedIndexScoreClass import *
from KindleReferencedIndexScoreDBs import *


class SnapshotDeal():
    DESIRABLE_PROCESS_NUM   = 1
    REFRESH_RATE            = float(0)
    LOOP_MESSAGE            = 'runnning as a deamon... you can exit with ctrl + c.'
    DIST_FILE_NAME          = 'snapshot.tmp'
    SRC_FILE_NAME           = 'src_snapshot.tmp'
    DIST_LDB_NAME           = 'snapshot.ldb'
    SRC_LDB_NAME            = 'src_snapshot.ldb'
    SCRAPING_DATA_POOL      = []
   
    """
    スタティックメソッドに何らかのデータがないならば、Noneを返す
    """
    @staticmethod
    def get_all():
        SnapshotDeal.charge_memory()
        return (lambda x:x if x != [] else None)( SnapshotDeal.SCRAPING_DATA_POOL )
    
    @staticmethod
    def get_all_ldb():
        db = plyvel.DB('./' + SnapshotDeal.DIST_LDB_NAME, create_if_missing=True)
        for (key, scraping_data) in db:
          scraping_data = pickle.loads(scraping_data.replace('', '\n') )
          yield scraping_data
        db.close()

    """
    無限ループすることでデーモンとして起動する
    """
    @staticmethod
    def run_as_a_deamon(limit):
        count = 0
        while True:
            """
            メモリ上のインスタンスを展開
            """
            SnapshotDeal.charge_memory()
            
            print(SnapshotDeal.LOOP_MESSAGE) 
            """
            古いデータを削除して強制的に上書きする
            """
            f = open(SnapshotDeal.SRC_FILE_NAME, 'w')
            #for (key, scraping_data, serialized) in initiate_data_generator():
            for (key, scraping_data) in get_all_data_iter():
                f.write(pickle.dumps(scraping_data).replace('\n', '') + '\n')
            
            """
            機能的に今は何も定義されていない
            """
            if limit == None:
                pass
            else:
                #for (key, scraping_data, serialized) in initiate_data_limit_generator(limit):
                #    f.write(serialized + '\n')
                pass
            f.close()
            
            """
            一時データを恒久的データのファイル名に変更
            """
            os.rename(SnapshotDeal.SRC_FILE_NAME, SnapshotDeal.DIST_FILE_NAME)
            
            
            """
            countをインクリメントして、limitと等しいか超えていたならば終了
            """
            count += 1
            if limit <= count:
                return
            """
            あまり頻度の高いリフレッシュはシステムに負荷をもたらすので、スリープする
            """
            time.sleep(SnapshotDeal.REFRESH_RATE)
    
    """
    通常のファイルシステムを利用せず、leveldbに書き出す。
    """
    @staticmethod
    def run_as_a_ldb_deamon(limit):
        count = 0
        while True:
            print(SnapshotDeal.LOOP_MESSAGE) 
            db = plyvel.DB('./' + SnapshotDeal.DIST_LDB_NAME, create_if_missing=True)
            for (key, scraping_data) in get_all_data_iter():
                if db.get(key) == None:
                  db.put(key, pickle.dumps(scraping_data).replace('\n', '') + '\n')
            db.close()
            
            """
            countをインクリメントして、limitと等しいか超えていたならば終了
            """
            count += 1
            if limit <= count:
                return
            """
            あまり頻度の高いリフレッシュはシステムに負荷をもたらすので、スリープする
            """
            time.sleep(SnapshotDeal.REFRESH_RATE)
    
    @staticmethod
    def charge_memory():
        """
        シリアライズ化されたデータよりもオブジェクトのインスタンスのほうがメモリは消費しない
        """
        scraping_data_list = []
        
        """
        ファイルが存在しない場合、処理を行わずreturnする
        """
        if not os.path.exists(SnapshotDeal.DIST_FILE_NAME):
            return

        for line in open(SnapshotDeal.DIST_FILE_NAME, 'r'):
            try:
                scraping_data_list.append(pickle.loads(line.replace('', '\n')))
            except pickle.UnpicklingError, e:
                print('[CRIT] [EXCEPT!] data may be broken! cannot restore instance from cache!', e)
                pass
            except UnicodeDecodeError, e:
                print('[CRIT] [EXCEPT!] cannot decode unicode error !')
                pass
        SnapshotDeal.SCRAPING_DATA_POOL = scraping_data_list
    
    @staticmethod
    def iter_all():
        """
        ファイルが存在しない場合、処理を行わずreturnする
        """
        if not os.path.exists(SnapshotDeal.DIST_FILE_NAME):
            yield None
        for line in open(SnapshotDeal.DIST_FILE_NAME, 'r'):
            try:
                yield  pickle.loads(line.replace('', '\n'))
            except pickle.UnpicklingError, e:
                print('[CRIT] [EXCEPT!] data may be broken! cannot restore instance from cache!', e)
                yield None
            except UnicodeDecodeError, e:
                print('[CRIT] [EXCEPT!] cannot decode unicode error !')
                yield None
"""
importされたらグローバル空間にインスタンスの展開をする
NOTE: あまりにもメモリをバカ食いするので、オンメモリは止めました
NOTE: importされたときのファイル名が__name__変数に入るので、実行時とモジュールロード時の動作がわけることができる
"""
if 'KindleReferencedIndexScoreDBsSnapshotDealer' == __name__:
    print('KindleReferencedIndexScoreDBsSnapshotDealer will be loaded')
    print('If you want to get all data as on-memory data, run charge_memory() at first.')

    SnapshotDeal.charge_memory()

"""
main文として実行されたら、以下の命令が実行される
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process Kindle Referenced Index Score.')
    parser.add_argument('--limit',   help='set limit num')
    parser.add_argument('--mode',     help='set mode')
    parser.add_argument('--refresh_rate',   help='set limit num')

    args_obj    = vars(parser.parse_args())
   
    limit       = (lambda x:int(x) if x else None)(args_obj.get('limit') )
    mode        = (lambda x:x if x else None)(args_obj.get('mode') )

    SnapshotDeal.REFRESH_RATE = (lambda x:x if x else SnapshotDeal.REFRESH_RATE)(args_obj.get('refresh_rate') )
    
    if mode == 'tmp' or mode == 'local':
      SnapshotDeal.run_as_a_deamon(limit)
    elif mode == 'leveldb' or mode == 'level':
      SnapshotDeal.run_as_a_ldb_deamon(limit)
