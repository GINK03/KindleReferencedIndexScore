# coding: utf-8
from __future__ import print_function
import bs4
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
    SCRAPING_DATA_POOL      = []
   
    """
    スタティックメソッドに何らかのデータがないならば、Noneを返す
    """
    @staticmethod
    def get_all():
        return (lambda x:x if x != [] else None)( SnapshotDeal.SCRAPING_DATA_POOL )
    
    """
    無限ループすることでデーモンとして起動する
    """
    @staticmethod
    def run_as_a_deamon():
        while True:
            """
            メモリ上のインスタンスを展開
            """
            SnapshotDeal.charge_memory()
            
            """
            古いデータを削除して強制的に上書きする
            """
            f = open(SnapshotDeal.SRC_FILE_NAME, 'w')
            for (key, scraping_data, serialized) in initiate_data_generator():
                f.write(serialized + '\n')
            f.close()
            
            """
            一時データを恒久的データのファイル名に変更
            """
            os.rename(SnapshotDeal.SRC_FILE_NAME, SnapshotDeal.DIST_FILE_NAME)
            
            print(SnapshotDeal.LOOP_MESSAGE) 
            
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
        for line in open(SnapshotDeal.DIST_FILE_NAME, 'r'):
            try:
                scraping_data_list.append(pickle.loads(line.replace('', '\n')))
            except pickle.UnpicklingError, e:
                print('[EXCEPT!] data may be broken! cannot restore instance from cache!', e)
                pass
            except UnicodeDecodeError, e:
                print('[EXCEPT!] cannot decode unicode error !')
                pass
        SnapshotDeal.SCRAPING_DATA_POOL = scraping_data_list
"""
importされたらグローバル空間にインスタンスの展開をする
NOTE: importされたときのファイル名が__name__変数に入るので、実行時とモジュールロード時の動作がわけることができる
"""
if 'KindleReferencedIndexScoreDBsSnapshotDealer' == __name__:
    print('module loaded')
    SnapshotDeal.charge_memory()


"""
main文として実行されたら、以下の命令が実行される
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process Kindle Referenced Index Score.')
    parser.add_argument('--refresh_rate',   help='set refresh rate')
    args_obj = vars(parser.parse_args())
    
    SnapshotDeal.REFRESH_RATE = (lambda x:x if x else SnapshotDeal.REFRESH_RATE)( args_obj.get('refresh_rate') )

    SnapshotDeal.run_as_a_deamon()
