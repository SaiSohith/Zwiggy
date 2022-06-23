import pandas as pd
import re
from website import scrapper as s
zomatodf = pd.read_csv('website\zomato.csv', encoding='latin-1')


def recommended():
    zomato = pd.read_csv('website\zomato.csv', encoding='latin-1')
    zf = zomato.nlargest(10, 'Votes')
    return zf.values.tolist()


def get_restaurant_names(d):
    ids = []
    names = []
    dic = {}
    ratings = []
    for i in range(len(d)):
        # dic[d[i][0]] = [d[i][1], d[i][-4]]
        ids.append(d[i][0])
        names.append(d[i][1])
        ratings.append(d[i][-4])
    data = [names, ids, ]
    return {'ids': ids, 'names': names, 'ratings': ratings}


def get_restaurant_details(id):
    zomatodf = pd.read_csv('website\zomato.csv',
                           encoding='latin-1', index_col='Restaurant Name')
    t = zomatodf.loc[id]
    # img = s.getrestaurant_img(t['Restaurant Name'])
    dat = [t['City'], t['Address'], t['Cuisines'], id]
    return dat


def searchrestaurant(name):
    results = []
    name = str(name)
    for i in zomatodf['Restaurant Name']:
        if re.match(name, i, re.IGNORECASE):
            results.append(i)
    return results
