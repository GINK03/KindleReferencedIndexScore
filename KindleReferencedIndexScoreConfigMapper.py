import os
import ConfigParser

class CM:
    KINDLE_URL          = 'https://www.amazon.co.jp/Kindle-%E3%82%AD%E3%83%B3%E3%83%89%E3%83%AB-%E9%9B%BB%E5%AD%90%E6%9B%B8%E7%B1%8D/b?ie=UTF8&node=2250738051'
    RETRY_NUM           = 10
    USER_AGENT          = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36'
    DESIRABLE_PROCESS_NUM = 1 
    SESSION_TOKEN       = '"ZN8mMEOqdcMl6ZsubV6h/95CPYeabI8vDHR7ef3qR/rxOqRWscUZG1DdUESiqODAxy7AjSQ4hMbl2VJW0BovH3236ZZAVHmpTj/y7cqXykNjxgYxCxqvdKaKYQ0sz6A3pxFgawd+g9POEzQ+Jd/MiWhRA45tJVVElx+MIeBHglU3i7RNm9EvIsMD50+6fKJnJkZMuTo/58vq62ThtF2ebOQNWltmWPP/Cs/0EzSOYRXlNXYcw/gJGokBipdFYA32US+3Ut/jb7bzNJ+ACDLYQA=="'

    
    @staticmethod
    def init():
        if os.path.isfile('settings.cnf'):
            config = ConfigParser.RawConfigParser()
            config.read('settings.cnf')
            CM.KINDLE_URL      = config.get('Section1', 'KINDLE_URL')
            CM.RETRY_NUM       = config.get('Section1', 'RETRY_NUM')
            CM.USER_AGENT      = config.get('Section1', 'USER_AGENT')
            CM.DESIRABLE_PROCESS_NUM = config.getint('Section1', 'DESIRABLE_PROCESS_NUM')
            CM.SESSION_TOKEN   = config.get('Section1', 'SESSION_TOKEN')
            return
        """
        settings.cnfがないならば、デフォルト値をセットして保存
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
