import os
import ConfigParser

class CM:
    KINDLE_URL          = 'https://www.amazon.co.jp/Kindle-%E3%82%AD%E3%83%B3%E3%83%89%E3%83%AB-%E9%9B%BB%E5%AD%90%E6%9B%B8%E7%B1%8D/b?ie=UTF8&node=2250738051'
    RETRY_NUM           = 10
    USER_AGENT          = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36'
    DESIRABLE_PROCESS_NUM = None
    SESSION_TOKEN       = None

    
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
        return
    
    @staticmethod
    def save():
        """
        $BCM$r%;%C%H$7$FJ]B8(B
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