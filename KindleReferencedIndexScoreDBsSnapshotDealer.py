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
    $B%9%?%F%#%C%/%a%=%C%I$K2?$i$+$N%G!<%?$,$J$$$J$i$P!"(BNone$B$rJV$9(B
    """
    @staticmethod
    def get_all():
        return (lambda x:x if x != [] else None)( SnapshotDeal.SCRAPING_DATA_POOL )
    
    """
    $BL58B%k!<%W$9$k$3$H$G4JC1$J%G!<%b%s$H$7$F5/F0$9$k(B
    """
    @staticmethod
    def run_as_a_deamon():
        while True:
            """
            $B%a%b%j>e$N%$%s%9%?%s%9$rE83+(B
            """
            SnapshotDeal.charge_memory()
            
            """
            $B8E$$%G!<%?$r:o=|$7$F6/@)E*$K>e=q$-$9$k(B
            """
            f = open(SnapshotDeal.SRC_FILE_NAME, 'w')
            for (key, scraping_data, serialized) in initiate_data_generator():
                f.write(serialized + '\n')
            f.close()
            
            """
            $B0l;~%G!<%?$r915WE*%G!<%?$N%U%!%$%kL>$KJQ99(B
            """
            os.rename(SnapshotDeal.SRC_FILE_NAME, SnapshotDeal.DIST_FILE_NAME)
            
            print(SnapshotDeal.LOOP_MESSAGE) 
            
            """
            $B$"$^$jIQEY$N9b$$%j%U%l%C%7%e$O%7%9%F%`$KIi2Y$r$b$?$i$9$N$G!"%9%j!<%W$9$k(B
            """
            time.sleep(SnapshotDeal.REFRESH_RATE)
    
    @staticmethod
    def charge_memory():
        """
        $B%7%j%"%i%$%:2=$5$l$?%G!<%?$h$j$b%*%V%8%'%/%H$N%$%s%9%?%s%9$N$[$&$,%a%b%j$O>CHq$7$J$$(B
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
import$B$5$l$?$i%0%m!<%P%k6u4V$K%$%s%9%?%s%9$NE83+$r$9$k(B
NOTE: import$B$5$l$?$H$-$N%U%!%$%kL>$,(B__name__$BJQ?t$KF~$k$N$G!"<B9T;~$H%b%8%e!<%k%m!<%I;~$NF0:n$,$o$1$k$3$H$,$G$-$k(B
"""
if 'KindleReferencedIndexScoreDBsSnapshotDealer' == __name__:
    print('module loaded')
    SnapshotDeal.charge_memory()


"""
main$BJ8$H$7$F<B9T$5$l$?$i!"0J2<$NL?Na$,<B9T$5$l$k(B
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process Kindle Referenced Index Score.')
    parser.add_argument('--refresh_rate',   help='set refresh rate')
    args_obj = vars(parser.parse_args())
    
    SnapshotDeal.REFRESH_RATE = (lambda x:x if x else SnapshotDeal.REFRESH_RATE)( args_obj.get('refresh_rate') )

    SnapshotDeal.run_as_a_deamon()
