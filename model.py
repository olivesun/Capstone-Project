import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD, NMF
from numpy.random import rand, RandomState
from numpy import array, matrix, linalg
from textblob import TextBlob
from collections import defaultdict
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
sentiment_d = {'Las Vegas':-0.3, 'Phoenix':-0.2}

def find_busienss_sufficient_bad_review(bad_review):
    '''
    INPUT a dataframe of bad review less or equal to 3 stars

    OUTPUT a list of businesses with more than 150 bad reviews that worth investigating
    '''

    mask = bad_review.business_id.value_counts().values>=60
    businesses = bad_review.business_id.value_counts().index[mask]
    return businesses

def reconst_mse(target, left, right):
    return (array(target - left.dot(right))**2).mean()

def describe_nmf_results(document_term_mat, W, H, n_top_words = 30):
    #print("Reconstruction error: %f") %(reconst_mse(document_term_mat, W, H))
    imp_words = []

    for topic in H:
        for i in topic.argsort()[:-n_top_words - 1:-1]:
            imp_words.append(feature_words[i])
    imp_words = set(imp_words)
    imp_words = list(imp_words)
    return imp_words

def make_sentences(review_df, business_id):
    data = review_df[review_df['business_id'] == business_id]
    doc_bodies = data['text'].values
    all_sentences = []
    for r in doc_bodies:
        sentences = r.lower().replace('\n','').replace('!','. ').replace('?','. ').split('. ')
        all_sentences.extend(sentences)
    return all_sentences, len(doc_bodies)


def find_aspects(sentences, city, n_top_words=15):
    '''
    INPUT sentences, city(str, lower case)
    OUTPUT aspects dictionary
    '''
    vectorizer = TfidfVectorizer(max_features=n_features, stop_words='english')
    document_term_mat = vectorizer.fit_transform(sentences)
    feature_words = vectorizer.get_feature_names()

    nmf = NMF(n_components=n_topics)
    W_sklearn = nmf.fit_transform(document_term_mat)
    H_sklearn = nmf.components_
    important_words = []

    for topic in H_sklearn:
        for i in topic.argsort()[:-n_top_words - 1:-1]:
                important_words.append(feature_words[i])
    important_words = set(important_words)
    important_words = list(important_words)

    nouns = []
    for i in sentences: nouns.extend(list(TextBlob(i).noun_phrases))
    noun_list = list(set(filter(lambda x: (len(x.split(' '))>1)&('...' not in x.split(' ')), nouns)))
    aspects_dict = defaultdict(list)

    for i in important_words:
        if i not in [city, city.lower(),'okay','ok','thing','things','time','times','greasy','awful'] and TextBlob(i).tags[0][1] in ['NN', 'NNS']:
            for j in noun_list:
                if i in j.split(' '):
                    aspects_dict[i].append(j)
    for i in aspects_dict: aspects_dict[i] = list(set(aspects_dict[i]))

    return aspects_dict

def find_summary(sentences, aspects_dict, topic, city):
    useful_sentences = []
    for sentence in sentences:
        for aspect in aspects_dict[topic]:
            if sentence.find(aspect)!= -1 and TextBlob(sentence).sentiment[0]<-sentiment_d[city]:
                useful_sentences.append(sentence)
    return list(set(useful_sentences))

    #return important_words, aspects, list(set(useful_sentences))

if __name__ == "__main__":
    bad_review = df_usres_rev[df_usres_rev['stars']<3]
    good_review_df = df_usres_rev[df_usres_rev['stars']==5]
    tips = df_usres_tip['text'].values
    businesses = find_busienss_sufficient_bad_review(bad_review)
    #print businesses

    n_features = 5000
    n_topics = 3
    business_id = businesses[int(raw_input('business index?'))]
    sens,quan= make_sentences(bad_review, business_id)
    aspects_d = find_aspects(sens,'Phoenix')
    print 'Hello owner of {0}, your restaurant has {1} 3- stars reviews :(( \
    we summaried somerepresentative sentences for you.'.format(business_id,quan)
    print 'here are the hot topic of bad reviews...'
    print aspects_d.keys()

    topic = str(raw_input('which topic are you interested?'))
    print find_summary(sens, aspects_d, topic, 'Phoenix')
    print 'would you like to which restaurants doing well on this topic?'
    if raw_input('yes/no ?') =='yes':
        print'please wait...'
        new_df = good_review_df[good_review_df['text'].str.contains(topic)]
        #new_df['text']=new_df['text'].apply(lambda x: x.replace('\n','').split('. '))
        good_business = list(set(new_df['business_id'].values))
        print df_usres_biz[['business_id', 'longitude','latitude']][df_usres_biz['business_id'].isin(good_business)].head()
