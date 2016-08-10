from flask import Flask
from flask import render_template
import pandas as pd
import make_file as mf
import review_analyze as ra
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD, NMF
from numpy.random import rand, RandomState
from numpy import array, matrix, linalg
from textblob import TextBlob
from collections import defaultdict
import sys

aspects_d = {}
sens = []
topics = []


app = Flask(__name__)



@app.route('/')
def index():

    return render_template('index.html')
@app.route ('/index')
def home():
    return render_template('index.html')

@app.route('/Solution1')
def Solution1():

    return render_template('Solution1.html')

@app.route('/tables')
def table():
    return render_template('tables.html')

@app.route('/how_it_work')
def how_it_work():
    return render_template('how_it_work.html')

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/Solution2')
def choose_city():
    res_names = df_bad['name'].values
    res_id = df_bad['business_id'].values
    data = zip(res_names,res_id)

    return render_template('Solution2.html',data = data)

@app.route('/bad_review/<biz_name>')
def analyze(biz_name=None):
    n_features = 5000
    n_topics = 3

    global sens
    sens= ra.make_sentences(bad_review, biz_name)
    global aspects_d
    aspects_d = ra.find_aspects(sens,'Phoenix')
    res_name = df_usres_biz['name'][df_usres_biz['business_id']==biz_name].values[0]
    global topics
    topics = aspects_d.keys()
    return render_template('topics.html', name=res_name, data=topics)

@app.route('/<name>/<topic>')
def summary(name=None, topic=None):
    global sens
    global aspects_d
    global topics
    summary = ra.find_summary(sens, aspects_d, topic, 'Phoenix')
    good_review_df = df_usres_rev[df_usres_rev['stars']==5]
    new_df = good_review_df[good_review_df['text'].str.contains(topic)]
    good_business = list(set(new_df['business_id'].values))
    good_res= df_usres_biz[['name', 'longitude','latitude']][df_usres_biz['business_id'].isin(good_business)].head().values
    good_res = good_res.tolist()
    item = topic
    return render_template('topics_details.html', item = item, name = name, summaries = summary, data = good_res, topics = topics)


if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding("utf-8")
    city = 'Phoenix'
    df_biz, df_review = mf.read_data()
    df_res_biz, df_res_rev = mf.make_restaurant(df_biz, df_review)
    df_usres_biz, df_usres_rev = mf.make_usa_restaurant(df_res_biz, df_res_rev, city)
    bad_review = df_usres_rev[df_usres_rev['stars']<3]
    businesses = ra.find_busienss_sufficient_bad_review(bad_review)
    df_bad = df_usres_biz[['business_id','name']][df_usres_biz['business_id'].isin(businesses)]
    app.run(host='0.0.0.0', port=7072, debug=True, threaded = True)
