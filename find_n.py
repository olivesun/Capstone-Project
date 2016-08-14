import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD, NMF
from numpy.random import rand, RandomState
from numpy import array, matrix, linalg
from textblob import TextBlob
from collections import defaultdict
from make_file import read_data,make_restaurant,make_usa_restaurant
import sys
import matplotlib.pyplot as plt
import seaborn as sns


reload(sys)
sys.setdefaultencoding("utf-8")

def reconst_mse(target, left, right):
    return (array(target - left.dot(right))**2).mean()

def describe_nmf_results(document_term_mat, W, H, n_top_words = 15):
    print("Reconstruction error: %f") %(reconst_mse(document_term_mat, W, H))
    for topic_num, topic in enumerate(H):
        print("Topic %d:" % topic_num)
        print(" ".join([feature_words[i] \
                for i in topic.argsort()[:-n_top_words - 1:-1]]))
    return

def lab(W):
    labels=[]
    for i in W:
        labels.append(i.argmax())
    return np.array(labels)

def make_sentences(x):
    all_sentences = []
    for r in x:
        sentences = r.lower().replace('\n','').replace('!','. ').replace('?','. ').split('. ')
        all_sentences.extend(sentences)
    return filter(lambda x: len(x.split(' '))>1, all_sentences)

def negative_score(x, n_topic,lst):
    score = 0

    vectorizer = TfidfVectorizer(stop_words='english')
    document_term_mat = vectorizer.fit_transform(x)
    feature_words = vectorizer.get_feature_names()

    nmf = NMF(n_components=n_topic)
    W= nmf.fit_transform(document_term_mat)
    H = nmf.components_
    important_words = []

    for topic in H:
        for i in topic.argsort()[:-10:-1]:
                important_words.append(feature_words[i])
    important_words = set(important_words)
    important_words = list(important_words)

    sentences  = make_sentences(x)

    nouns = []
    for i in sentences: nouns.extend(list(TextBlob(i).noun_phrases))
    noun_list = list(set(filter(lambda x: (len(x.split(' '))>1)&('...' not in x.split(' ')), nouns)))
    aspects_dict = defaultdict(list)

    for i in important_words:
        if i not in lst and TextBlob(i).tags[0][1] in ['NN', 'NNS']:
            for j in noun_list:
                if i in j.split(' '):
                    aspects_dict[i].append(j)
    for i in aspects_dict: aspects_dict[i] = list(set(aspects_dict[i]))

    useful_sentences = []
    topics = set()
    aspects = set()
    num =0
    for sentence in sentences:
        for topic in aspects_dict.keys():
            for aspect in aspects_dict[topic]:
                if sentence.find(aspect)!= -1 and TextBlob(sentence).sentiment[0]<0:
                    useful_sentences.append(sentence)
                    score += TextBlob(sentence).sentiment[0]
                    num +=1
                    topics.add(topic)
                    aspects.add(aspect)
    return score/len(topics)

if __name__ == '__main__':
    city = str(raw_input('Hello! Please enter city of interest...'))
    print 'preparing files... please wait.'
    df_biz, df_review = read_data()
    df_res_biz, df_res_rev = make_restaurant(df_biz, df_review)
    df_usres_biz, df_usres_rev= make_usa_restaurant(df_res_biz, df_res_rev, city)
    bad_review = df_usres_rev[df_usres_rev['stars']<3]
    lst =['okay','ok','thing','things','time','times','greasy','awful','review','oh','sorry','restaurant'\
    'restaurants','reviews','experiece','alice','unit','man','dry','hour','lo','food','drink','minute','minutes','cute','luck','excellent','friend'\
    'elephant','decent','thai','hut','friends','restaurant','restaurants','decent','soooo','bears','people','friend','mom','children','list','loss',\
    'los','table']
    n_topics = 10

    b_list = ['KjymOs12Mpy0Kd54b7T9MA','ngNvH4sxnH9aMukTZ67R_Q','QbmcCE_cLq4WO8ZMKImaLw','aGbjLWzcrnEx2ZmMCFm3EA','YNQgak-ZLtYJQxlDwN-qIg','zt1TpTuJ6y9n551sw9TaEg']
    for i, b in enumerate(b_list):
        locals()['bad_{0}'.format(i+1)] = bad_review[bad_review['business_id']==b_list[i]]
        locals()['x{0}'.format(i+1)] = locals()['bad_{0}'.format(i+1)]['text'].values
    print "start analysing!"

    x_axis = range(2,30)
    neg1=[]
    neg2=[]
    neg3=[]
    neg4=[]
    neg5=[]
    neg6=[]
    for i in x_axis:

        #neg1.append(negative_score(x1, i, lst))
        #neg2.append(negative_score(x2, i, lst))
        neg3.append(negative_score(x3, i, lst))
        neg4.append(negative_score(x4, i, lst))
        neg5.append(negative_score(x5, i, lst))
        neg6.append(negative_score(x6, i, lst))
    plt.plot(x_axis,neg3,label='150-250 reviews')
    plt.plot(x_axis,neg4,label='250-350 reviews')
    plt.plot(x_axis,neg5,label='350-450 reviews')
    plt.plot(x_axis,neg6,label='450-550 reviews')

    plt.show()
