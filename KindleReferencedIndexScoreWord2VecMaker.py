# coding: utf-8
from gensim import corpora, models, similarities
from gensim.models import word2vec
import time
import sys
import string, codecs
from hashlib import md5
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
def flatten_tokens(texts):
    documents = ["Human machine interface for lab abc computer applications",
                 "A survey of user opinion of computer system response time",
                 "The EPS user interface management system",
                 "System and human system engineering testing of EPS",
                 "Relation of user perceived response time to error measurement",
                 "The generation of random binary unordered trees",
                 "The intersection graph of paths in trees",
                 "Graph minors IV Widths of trees and well quasi ordering",
                 "Graph minors A survey"]

    # remove common words and tokenize
    stoplist = set('for a of the and to in'.split())

    print '[INFO] Start count words...'
    start = time.time()
    from itertools import chain
    #corpus = [str(md5(x.replace('[','').replace(']', '')).hexdigest()) for x in list(chain.from_iterable(texts))]
    corpus = [x.replace('[','').replace(']', '').replace(' ', '_') for x in list(chain.from_iterable(texts))]
    print '[INFO] End count words... Elapsed time', time.time() - start
    
    
    dictionary = corpora.Dictionary(texts)
    dictionary.save('./tmp/word2vec.dict') # store the dictionary, for future reference
    #with open('./tmp/text8corpus.txt', 'w') as f:
    with open('./tmp/text8corpus.txt', 'a') as f:
        f.write( ' '.join(corpus)) 

def extra():
    sentences = word2vec.Text8Corpus('./mini_text8')
    model = word2vec.Word2Vec(sentences, size=200) 
    model.save("sample.model")
    sampleinput = set()
    with open('./mini_text8') as f:
        [sampleinput.add(w) for w in f.read().split(' ') ]
    for w in sampleinput:
        try:
            s(w)
            print w 
        except:
            pass

def dealmodel(corpus_file = './tmp/text8corpus.txt', save = './tmp/text8.model'):
    data = word2vec.Text8Corpus(corpus_file)
    model = word2vec.Word2Vec(data, size=50, min_count=1)
    model.save(save)
    for k in model.vocab.keys():
        print k

def most_similar(posi, nega=[], n=5, tgt_model = './tmp/text8.model'):
    cnt = 1
    model = word2vec.Word2Vec.load(tgt_model)
    result = model.most_similar(positive = posi, negative = nega, topn = n)
    for r in result:
        print cnt, r[0], r[1]
        cnt += 1

def dump_keys():
    model = word2vec.Word2Vec.load('./tmp/text8.model')
    for k in model.vocab.keys():
        print k
if __name__ == '__main__':
    import plyvel
    import msgpack
    
    if '-d' in sys.argv:
        db = plyvel.DB('./tmp/word2vec_corpus.ldb' , create_if_missing=True)
        texts = []
        for k, raw in db:
            loaded = msgpack.unpackb(raw)
            if type(loaded) is list:
                texts.append( loaded)
            flatten_tokens(texts)
        db.close()
    
    if '-dmm-d' in sys.argv:
        texts = []
        with open('./query-expansion/dmm_wakati.txt') as f:
            texts = f.read().split('\n')
        for text in texts:
            try:
                print text.decode('utf-8')
            except UnicodeDecodeError:
                pass
            pass
        
    if '-m' in sys.argv:
        #with open('./tmp/text8corpus.txt', 'r') as f:
        #    f.read()
        dealmodel()
    
    if '-dmm-m' in sys.argv:
        dealmodel('./query-expansion/dmm_wakati_utf8.txt', './tmp/dmm.model')
    
    if '-e' in sys.argv:
        # '-p:' in sys.argv[2]
        print sys.argv[2].decode('utf-8')
        pwords = [x.decode('utf-8') for x in sys.argv[2].split(':')[1:] ]
        most_similar(pwords, [], 20, './tmp/text8.model')

    if '-dmm-e' in sys.argv:
        # '-p:' in sys.argv[2]
        print sys.argv[1].decode('utf-8')
        pwords = [x.decode('utf-8') for x in sys.argv[2].split(':')[1:] ]
        most_similar(pwords, [], 20, './tmp/dmm.model')

    if '-k' in sys.argv:
        dump_keys()
