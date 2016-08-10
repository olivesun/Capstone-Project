import pandas as pd

def read_data():
    df_biz = pd.read_csv('data/business.csv')
    df_review = pd.read_csv('data/review.csv')
    #df_user = pd.read_csv('data/user.csv')
    #df_checkin = pd.read_csv('data/checkin.csv')
    #df_tip = pd.read_csv('data/tip.csv')
    return df_biz, df_review#, df_user, df_checkin, df_tip

def make_restaurant(df_biz, df_review):
    df_res_biz = df_biz[df_biz['categories'].str.contains('Restaurants' or 'Food' or 'Bars')]
    restaurants = df_res_biz['business_id']
    df_res_rev = df_review[df_review['business_id'].isin(restaurants)]
    return df_res_biz, df_res_rev

def make_pair(df):
    df1 = df[['business_id', 'user_id']]
    return df1

def make_good_review_pair(df):
    df1 = df[df['stars']>=4]
    df1 = df1[['business_id', 'user_id']]
    review_counts = df1['business_id'].value_counts().values
    mask = review_counts>20
    hot_restaurants = df1['business_id'].value_counts().index[mask]
    df1 = df1[df1['business_id'].isin(hot_restaurants)]
    return df1

def make_usa_restaurant(df_res_biz, df_res_rev, city):
    df_usres_biz = df_res_biz[df_res_biz['city'].isin([city])]
    us_restaurants = df_usres_biz['business_id']
    df_usres_rev = df_res_rev[df_res_rev['business_id'].isin(us_restaurants)]
    #df_usres_tip = df_res_tip[df_res_tip['business_id'].isin(us_restaurants)]
    #df_usres_checkin = df_res_checkin[df_res_checkin['business_id'].isin(us_restaurants)]
    return df_usres_biz, df_usres_rev #df_usres_checkin, df_usres_tip

def make_usa_restaurant_review(df_biz, city):
    df_usa = df_biz[df_biz['city'].isin([city])]
    us_biz = df_usa['business_id']
    us_review = df_review[df_review['business_id'].isin(us_biz)]
    return us_review

def save_txt(df):
    df.to_csv(r'pair_test_LV.txt', header=None, index=None, sep=' ')
    return

def train_test_sep(df):
    df_train = df[df['date']<'2015-01-01']
    df_test = df[df['date']>='2015-01-01']
    return df_train, df_test

if __name__ == '__main__':
    city = str(raw_input('Hello! Please enter city of interest...'))
    print 'preparing files... please wait.'
    df_biz, df_review = read_data()
    df_res_biz, df_res_rev = make_restaurant(df_biz, df_review)
    df_usres_biz, df_usres_rev= make_usa_restaurant(df_res_biz, df_res_rev, city)
    usres_rev_train, usres_rev_test = train_test_sep(df_usres_rev)
    #us_review = make_usa_review()
    #review_pair = make_pair(df_review)
    #good_review_pair = make_good_review_pair(usres_rev_train)
    #save_txt(good_review_pair)
    bad_review = df_usres_rev[df_usres_rev['stars']<=3]
