import os
import ConfigParser

class CM:
    KINDLE_URL          = 'https://www.amazon.co.jp/Kindle-%E3%82%AD%E3%83%B3%E3%83%89%E3%83%AB-%E9%9B%BB%E5%AD%90%E6%9B%B8%E7%B1%8D/b?ie=UTF8&node=2250738051'
    RETRY_NUM           = 10
    USER_AGENT          = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36'
    DESIRABLE_PROCESS_NUM = None
    SESSION_TOKEN       = None
    HTTP_WAIT_SEC       = 2
    DESIRABLE_PROCESS_NUM_SQL = 10
    LEVELDB_SHADOW_TINDEX = 'shadow_snapshot.ldb'
    KINDLE_UNLIMITED_SPECIAL_WORDS = 'Kindle Unlimited会員の方は読み放題でお楽しみいただけます'
    DEFAULT_IDFDIC      = './stash/idf_base_27gb_snapshot_index40000shuf.txt' 
    DEFAULT_TINDEX_URL_TERM = 'tindex_url_term.ldb'

    @staticmethod
    def init():
        my_file = (os.path.join(os.getcwd(),'settings.cfg'))
        config = ConfigParser.RawConfigParser()
        config.read(my_file)
        CM.KINDLE_URL      = config.get('Section1', 'KINDLE_URL')
        CM.RETRY_NUM       = config.get('Section1', 'RETRY_NUM')
        CM.USER_AGENT      = config.get('Section1', 'USER_AGENT')
        CM.DESIRABLE_PROCESS_NUM = config.getint('Section1', 'DESIRABLE_PROCESS_NUM')
        CM.SESSION_TOKEN   = config.get('Section1', 'SESSION_TOKEN')
        CM.HTTP_WAIT_SEC   = config.getint('Section1', 'http_waitsec')
        CM.SQL_IP          = config.get('Section1', 'SQL_IP')
        CM.DESIRABLE_PROCESS_NUM_SQL = config.getint('Section1', 'DESIRABLE_PROCESS_NUM_SQL')
        CM.LEVELDB_SHADOW_TINDEX = config.get('Section1', 'LEVELDB_SHADOW_TINDEX')
        CM.KINDLE_UNLIMITED_SPECIAL_WORDS = config.get('Section1', 'KINDLE_UNLIMITED_SPECIAL_WORDS').decode('utf-8')
        CM.DEFAULT_IDFDIC  = config.get('Section1', 'DEFAULT_IDFDIC')
        CM.DEFAULT_TINDEX_URL_TERM = config.get('Section1', 'DEFAULT_TINDEX_URL_TERM')
        return
    
    @staticmethod
    def save():
        """
        値をセットして保存
        """
        with open('settings.cfg', 'wb') as configfile:
            config = ConfigParser.RawConfigParser()
            config.add_section('Section1')
            config.set('Section1', 'KINDLE_URL',    CM.KINDLE_URL )
            config.set('Section1', 'RETRY_NUM',     CM.RETRY_NUM  )
            config.set('Section1', 'USER_AGENT',    CM.USER_AGENT )
            config.set('Section1', 'DESIRABLE_PROCESS_NUM', CM.DESIRABLE_PROCESS_NUM )
            config.set('Section1', 'SESSION_TOKEN', CM.SESSION_TOKEN )
            config.write(configfile)

CM.init()
