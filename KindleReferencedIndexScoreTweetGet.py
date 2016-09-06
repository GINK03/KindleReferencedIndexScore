import requests
from requests_oauthlib import OAuth1
import json
import datetime


api_key = "14ANSXlBRKVz8GKwaMM6KTcKv"
api_secret = "ExdUchkPlkFpXElz1OBLqJ84JR9TT5C9tqDU2XdFBMqO95sKjG"
access_token = "2343754692-2trgvPdZwkx23V4n6PUNulwD1hxCCXtcIjPCaEQ"
access_secret = "djF6aAONRpZsuMMXx1hbtQmdWHXeCo535YZOmsYExAJ44"
url = "https://stream.twitter.com/1.1/statuses/sample.json"

auth = OAuth1(api_key, api_secret, access_token, access_secret)

r = requests.post(url, auth=auth, stream=True )

with open('./tweets/dump' + str(datetime.datetime.now()), 'w' ) as f:
  for line in r.iter_lines():
    try:
      data = json.loads(line)
    except:
      continue
    if data.get("user") and data["user"]["lang"] != "ja":
      continue
    if data.get("text") is None:
      continue
    """sample time
    Tue Sep 06 02:33:10 +0000 2016
    '%a %b %d %H:%M:%S +0000 %Y'
    """
    stime = data.get("created_at")
    tdatetime = datetime.datetime.strptime(stime, '%a %b %d %H:%M:%S +0000 %Y')
    line = " ".join( ["[TEXT]", data.get("text").encode('utf-8'), "[CREATED_AT]", str(tdatetime)] )
    print "[TEXT]", data.get("text"), "[CREATED_AT]", str(tdatetime)
    f.write(line)
