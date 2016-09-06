# coding: utf-8
import requests
from requests_oauthlib import OAuth1
import json
import datetime


def get_sample():
    api_key = "14ANSXlBRKVz8GKwaMM6KTcKv"
    api_secret = "ExdUchkPlkFpXElz1OBLqJ84JR9TT5C9tqDU2XdFBMqO95sKjG"
    access_token = "2343754692-2trgvPdZwkx23V4n6PUNulwD1hxCCXtcIjPCaEQ"
    access_secret = "djF6aAONRpZsuMMXx1hbtQmdWHXeCo535YZOmsYExAJ44"
    url = "https://stream.twitter.com/1.1/statuses/sample.json"

    auth = OAuth1(api_key, api_secret, access_token, access_secret)

    r = requests.post(url, auth=auth, stream=True )

    with open('./tweets/dump' + str(datetime.datetime.now()).replace(' ', '_'), 'w' ) as f:
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
        text = data.get("text").replace('\n', ' ').encode('utf-8')
        line = "".join( [ text, "[D]", str(tdatetime), "\n"] )
        print line,
        f.write(line)

import sys
import gensim
from gensim.models import word2vec
def tweets_word2vec():
    fname = sys.argv[2]
    print fname
    sentence = word2vec.Text8Corpus(fname)
    model = word2vec.Word2Vec(sentence, size=200, min_count=20, window=15)
    model.save("tweets.model")

import regex
def trim():
    for line in sys.stdin:
        line = line.strip().split('[D]').pop(0)
        trimmed = regex.sub('@[a-zA-Z0-9_]{1,}', '', line)
        trimmed = regex.sub('RT', '', trimmed)
        trimmed = regex.sub('http(s)?://([\w-]+\.)+[\w-]+(/[\w- ./?%&=]*)?', '', trimmed)
        #print line
        print trimmed

def mostsim():
    # 学習済みモデルのロード
    model = word2vec.Word2Vec.load("tweets.model")

    # 入力された単語から近い単語をn個表示する
    def s(posi, nega=[], n=10):
	cnt = 1 # 表示した単語の個数カウント用
	# 学習済みモデルからcos距離が最も近い単語n個(topn個)を表示する
	result = model.most_similar(positive = posi, negative = nega, topn = n)
	for r in result:
	    print cnt,'　', r[0],'　', r[1]
	    cnt += 1
    s(["live".encode('utf-8')])
    s(["私".decode('utf-8')])
    s(["テスト".decode('utf-8')])
    s(["おっぱい".decode('utf-8')])
    s(["ポケモンGO".decode('utf-8')])
    s(["アニメ".decode('utf-8')])
    s(["iPhone".decode('utf-8')])


if __name__ == '__main__' :
    if '-g' in sys.argv:
        get_sample()
    if '--tweets' in sys.argv:
        tweets_word2vec()
    if '--trim' in sys.argv:
        trim()
    if '--mostsim' in sys.argv:
        mostsim()
