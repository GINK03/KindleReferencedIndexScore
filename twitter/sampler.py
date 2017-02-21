import json
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import re
ACCESS_TOKEN = '2343754692-NagKE0CwUjHpe3hZNNdxdtJnavox5XmPPc8G675'
ACCESS_SECRET = ''
CONSUMER_KEY = 'XvvFplttoVqGzYublMqtEDRYR'
CONSUMER_SECRET = ''

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_stream = TwitterStream(auth=oauth)
iterator = twitter_stream.statuses.sample()
for tweet in iterator:
  lang = tweet.get('lang')
  if lang and lang.lower() == 'ja':
    screen_name = tweet.get('user').get('screen_name')
    print('sc', screen_name)
    created_at  = tweet.get('created_at')
    e, m, d, time, fix, year = created_at.split()
    fixed_time  = "%s_%s_%s_%s"%(year, m, d, time)
    print(fixed_time)
    text        = re.sub('http.*? ', ' ', tweet.get('text').replace('\n', ' '))
    text        = re.sub('@.*? ', ' ', text)
    text        = re.sub('http.*?$', '', text)
    text        = re.sub('RT\s{1,}', '', text)
    
    if tweet.get('retweeted_status') is None:
      favs        = tweet.get('favorite_count')
      print("fv nn", favs)
      rt_status   = tweet.get('retweet_count')
      print("rt nn", rt_status)
      filename = "out/%s_%s"%(fixed_time, screen_name)
      friends     = tweet.get('user').get('friends_count')
      print("fr", friends)
      print("tx", text)
      obj = {'favs':favs, 'rt':rt_status, 'txt':text, 'fr':friends } 
      open(filename, 'w').write(json.dumps(obj))
      continue

    if tweet.get('retweeted_status') is not None:
      #print(json.dumps(tweet, indent=4))
      friends_nested     = tweet.get('retweeted_status').get('user').get('friends_count')
      screen_name_nested = tweet.get('retweeted_status').get('user').get('screen_name')
      created_at_nested  = tweet.get('retweeted_status').get('user').get('created_at')
      e, m, d, time, fix, year = created_at_nested.split()
      fixed_time_nested  = "%s_%s_%s_%s"%(year, m, d, time)
      print("nsc ", screen_name_nested)
      print("nca ", fixed_time_nested)
      favs        = tweet.get('retweeted_status').get('favorite_count')
      print("fv en", favs)
      rt_status   = tweet.get('retweeted_status').get('retweet_count')
      print("rt en", rt_status)
      print("tx", text)
      filename = "out/%s_%s"%(fixed_time_nested, screen_name_nested)
      obj = {'favs':favs, 'rt':rt_status, 'txt':text , 'fr':friends_nested } 
      open(filename, 'w').write(json.dumps(obj))
      #url         = tweet.get('retweeted_status').get('entities').get('urls').get('expanded_url')
      #print("url", url)
