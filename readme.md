# Restaurant Owner Navigator

Identify Potential Customers, Analyze Current Problems, and More with Yelp Dataset

## Overview

The goal of the project is to help individual business owner to refine marketing strategy therefore lower customer acquisition cost, and tackle the reviews with bad ratings. It has two parts: Marketing Solution and Improvement Solution.

### Approach

For marketing solution, similar users are identified by finding similar users to people who already gave 4+ star ratings to your business. These people should be targeted audience for advertising on Yelp.

```
Similar Users: those who share N+ number of restaurants they left 4+ ratings to
N ranging from 5 to 10 are tried to compare results.
```

For improvement solution, food items that were major topics are identified and original reviews on these food items are presented. Restaurants nearby that are doing well on these food items are also suggested.


### WebApp

A demo for this project can be find [here](http://0.0.0.0:7072/).


## Solutions

### Data

Data is transformed from `json` file to `csv`  for better exploration. Only data for the city of Las Vegas (4658 businesses & 501631 reviews) and Phoenix (2922 businesses & reviews) are used. And they yield similar results. To load data faster, the webapp use city of Phoenix as an example, but it is possible to scale.

### Marketing Solution

Advertising is NOT expensive. According to Yelp, business can spend $1,000 for 10,000 targeted impressions or $3.27 per click. By targeted, Yelp places your ads on competitor pages and highly targeted searches in your city. However, these 10,000 targeted impressions only results in 10 customers and 2 reviewers, with an already very optmistic 2% CTR, 5% of conversion rate and 20% review rate. You need customers and reviewers. Not just impressions& clicks!

Getting customers and reviewers are therefore extremely expensive. It takes $100 to get one customer, and $500 to get a reviewer!

I used MapReduce to find out similar users by MRJob package. N from 5 to 10 are tried upon and it turns out that:

```
with increase of N, it become more likely these similar users who have never been to your business will come to visit the restaurants, and leave reviews.
```

By finding similar users to people who already liked and left positive reviews, we help business to target the right audience and increase your advertising efficiency. Data shows these similar users are 2-7 times more likely to review your restaurants, and estimately 4 times more likely to be your customers. Finding the right people are important to your business.

### Improvement Solution

To analyze bad reviews, I used Non-Negative Matrix factorization to do topic modeling. Different combinations of number of topic, number of features and number of top words are tried out to test how accurate model is able to get the topics (mostly food items) in the reviews. The optimal combination is used for the final model.

These words in hot topics then were cross-examined with the noun phrases in bad reviews to establish the aspects that the restaurant is interested in. They are mostly food items, service, environment and location. Original sentences with these aspects are re-presented and filtered by sentiment score. Negative ones are preserved and shown.

By selecting the aspect interested, business owners can also check which nearby restaurants get 5-stars on these aspect. Maybe they can check it out themselves to find out why people love it!

## Running on your Own

For EDA, run `make_file.py` and `train_test.py` to test the enhancement of efficiency of selective marketing audience.

The `model.py` files contains the functions established for natural language processing models. They can be run together as a file or separately.

```
To try on different similarities by choosing N, please change the file name according to files in the folder 'user_similarity'.
```

To launch the webapp, run `app1.py` in `app` folder.

## Built With

* Webapp: Flask, html, css, javascript
* Modelling: Python sklearn for NMF and TFIDF, TextBlob for POS tags of words and sentiment analysis
* Other techniques: Morris chart, MRjob of MapReduce


## Acknowledgments

* Dataset is from Yelp dataset challenge
* Reference is made to 'An Unsupervised Aspect-Sentiment Model for Online Reviews' co-authored by Samuel Brody and Noemie Elhadad
