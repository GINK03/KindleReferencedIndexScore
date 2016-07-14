# coding: utf-8
import bs4
import sys
import urllib2
import urllib
import os.path
import __future__
import argparse
import multiprocessing as mp
import threading
import datetime
import sys
import time
from KindleReferencedIndexScoreClass import *
from KindleReferencedIndexScoreDBs import *

# defined parameters
DESIRABLE_PROCESS_NUM   = 1
RFRESH_RATE             = 300

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process Kindle Referenced Index Score.')
    parser.add_argument('--refresh_rate',   help='set refresh rate')
    args_obj = vars(parser.parse_args())
    
    REFRESH_RATE = args_obj.get('refresh_rate')

    for (key, scraping_data) in initiate_data_generator():



