import os
import sys
for _ in range(10000):
  os.system('echo %s | python3 adhocYahooXMLParserFileSystem.py -c'%sys.argv[1])
