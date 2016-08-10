from __future__ import division
import pandas as pd

df_similar = pd.read_csv('user_simi/Phoenix_test7', header = None, delimiter='\t')
df_similar.columns = ['user_id','similar_user_list']
df_similar = pd.read_csv('user_simi/LV_test10', header = None, delimiter='\t')
df_similar.columns = ['user_id','similar_user_list']
df_similar = pd.read_csv('count00', header = None, delimiter='\t')

def find_testing_business(df_test, df_train):
    '''
    OUTPUT a list of business that can be tested on similarity

    '''
    test_business_ids_mask = df_test.business_id.value_counts().values>=100
    test_business_ids = df_test.business_id.value_counts().index[test_business_ids_mask]
    s_test = set(test_business_ids)
    train_business_ids_mask = df_train.business_id.value_counts().values>=20
    train_business_ids = df_train.business_id.value_counts().index[train_business_ids_mask]
    s_train = set(train_business_ids)
    return s_test.intersection(s_train)

def find_customers(business, df_test, df_train, df_similar):
    '''
    INPUT business ID, testing dataframe(review in 2015), and similar_user dataframe(before 2015)
    OUTPUT an array of customers who left review (assume they came in 2015)
    '''
    customer_2015_business = set(df_test['user_id'][df_test['business_id'] == business].values)
    #customer_2015_list = set(df_business_2015['user_id'].values)
    old_customers_business = set(df_train['user_id'][df_train['business_id']==business].values)
    #df_train_goodreview = df_train[df_train['stars']>=4]
    #df_test_goodreview = df_test[df_test['stars']>=4]
    #df_business_goodreview2015 = df_test_goodreview[df_test_goodreview['business_id']==business]
    #df_business_pre2015= df_train_goodreview[df_train_goodreview['business_id'] ==business]
    fan_list_pre2015 = set(df_train['user_id'][(df_train['stars']>=4)&(df_train['business_id'] == business)].values)
    fan_list_2015 = set(df_test['user_id'][(df_test['stars']>=4)&(df_test['business_id'] == business)].values)
    similar_fans = list()
    for fan in list(fan_list_pre2015):
        if df_similar['similar_user_list'][df_similar['user_id']==fan].values:
            similar_users = df_similar['similar_user_list'][df_similar['user_id']==fan].values[0].split(', ')
            for similar_user in similar_users:
                similar_fans.append(similar_user.strip('["]'))
    new_similar_users = set(similar_fans).difference(old_customers_business)
    #return len(fan_list_pre2015), len(customer_2015_list), len(new_similar_users), len(fan_list_2015)
    return fan_list_pre2015, customer_2015_business, new_similar_users, fan_list_2015

def testing_new_customer(fan_list_pre2015, customer_2015_business, new_similar_users, fan_list_2015):
    '''
    INPUT three SETS
    OUTPUT number of new customers in 2015, percentage of similar users identified
    actually came, percentage of identified users in new customers
    '''
    similar_users_came_2015 = new_similar_users.intersection(customer_2015_business)
    similar_users_fan_2015 = new_similar_users.intersection(fan_list_2015)
    new_customers = customer_2015_business.difference(fan_list_pre2015)
    proportion_in_new_customer = len(similar_users_came_2015)*1.0/len(new_customers)
    proportion_in_similar_users = len(similar_users_came_2015)*1.0/len(new_similar_users)
    proportion_goodreview_similar_users = len(similar_users_fan_2015)*1.0/(len(similar_users_came_2015)+0.01)
    #return len(similar_users_fan_2015),len(similar_users_came_2015), len(new_similar_users)
    return len(new_customers), proportion_in_similar_users, proportion_in_new_customer, proportion_goodreview_similar_users

def baseline_new_customer(business, df_test, df_train):
    customers_2015_all = set(df_test['user_id'].values)
    old_customers_all = set(df_train['user_id'].values)
    all_customers = customers_2015_all.union(old_customers_all)
    customers_2015_business = set(df_test['user_id'][df_test['business_id']==business].values)
    old_customers_business = set(df_train['user_id'][df_train['business_id']==business].values)
    customers_2015_good_business = set(df_test['user_id'][(df_test['business_id']==business)\
    &(df_test['stars']>=4)].values)
    new_fan_business = customers_2015_good_business.difference(old_customers_business)
    new_customer_business = customers_2015_business.difference(old_customers_business)
    new_potential_customers = all_customers.difference(old_customers_business)
    #return new_fan_business, customers_2015_business, customers_2015_good_business
    return len(new_customer_business)*1.0/len(new_potential_customers), len(new_fan_business)*1.0/(len(new_customer_business)+0.01)
    #return len(customers_2015_all), len(customers_2015_business), len(old_customers_business), len(new_customer_business), len(new_potential_customers)



if __name__=='__main__':
    businesses = find_testing_business(usres_rev_test, usres_rev_train)
    accuracy_list = []
    portion_list = []
    good_list = []
    baseline_list = []
    baseline_good_list = []
    for business in list(businesses):
        fan_list_pre2015, customer_2015_business, new_similar_users, fan_list_2015 =\
        find_customers(business, usres_rev_test, usres_rev_train, df_similar)
        new_customer_number, accuracy, portion, good_review_portion = \
        testing_new_customer(fan_list_pre2015, customer_2015_business, new_similar_users, fan_list_2015)
        accuracy_list.append(accuracy)
        portion_list.append(portion)
        good_list.append(good_review_portion)
        baseline, baseline_good = baseline_new_customer(business, usres_rev_test, usres_rev_train)
        baseline_list.append(baseline)
        baseline_good_list.append(baseline_good)
        #print 'business: {0}- In 2015, your restaurant has {1} new customers,\n out of them \
        #{4} are the identified similar users, {2} of them left good ratings, \
        #and {3} of identified similar users did visit!'\
        #.format(business, new_customer_number, good_review_portion, accuracy, portion)

    import numpy as np
    accuracy_list = np.array(accuracy_list)
    portion_list = np.array(portion_list)
    good_list = np.array(good_list)
    baseline_list = np.array(baseline_list)
    baseline_good_list = np.array(baseline_good_list)
    print 'averagely, {0} similar users identified left reviews to restaurants,{1} of them left more than \
    4 starts rating! {2} new customers are identified'\
    .format(accuracy_list.mean(), good_list.mean(), portion_list.mean())
    print 'compare to averagely, {0} of users leave review to the restaurants, and {1} of them left good rating.\
    '.format(baseline_list.mean(), baseline_good_list.mean())


'''
    o = 0
    for business in list(businesses):
        a,b,c,d =find_customers(business, usres_rev_test, usres_rev_train, df_similar)
        print testing_new_customer(a,b,c,d)

        o+=1
'''
