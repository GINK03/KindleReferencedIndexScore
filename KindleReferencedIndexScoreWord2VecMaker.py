# coding: utf-8
from gensim import corpora, models, similarities
from gensim.models import word2vec

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
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]

# remove words that appear only once
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once]
         for text in texts]

print all_tokens

dictionary = corpora.Dictionary(texts)
dictionary.save('/tmp/deerwester.dict') # store the dictionary, for future reference
print dictionary

print dictionary.token2id


new_doc = "Human computer interaction"
new_vec = dictionary.doc2bow(new_doc.lower().split())
print new_vec # the word "interaction" does not appear in the dictionary and is ignored

#sentences = word2vec.Text8Corpus('wakati_kankore.txt')
sentences = word2vec.Text8Corpus('./mini_text8')
model = word2vec.Word2Vec(sentences, size=200) 
model.save("sample.model")
sampleinput = set()
with open('./mini_text8') as f:
    [sampleinput.add(w) for w in f.read().split(' ') ]
def s(posi, nega=[], n=5):
    cnt = 1
    result = model.most_similar(positive = posi, negative = nega, topn = n)
    for r in result:
        print cnt, r[0], r[1]
        cnt += 1
for w in sampleinput:
    try:
        s(w)
        print w 
    except:
        pass

