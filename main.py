import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import cross_val_score

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Lasso
from sklearn.tree import DecisionTreeRegressor





matplotlib.rcParams["figure.figsize"] = (20,10)

df1 = pd.read_csv("house-price-cities-Texas.csv")

df2 = df1.drop(['Condition'], axis ='columns')


df3 = df2.copy()
df3['price_per_sqft'] = df3['Price']/df3['Total-Sqft']

df3.Location.apply(lambda x: x.strip())

location_stats = df3.groupby('Location')['Location'].agg('count').sort_values(ascending=True)


location_stats_less_than_8 = location_stats[location_stats<=8]

df3.Location = df3.Location.apply(lambda x: 'other' if x in location_stats_less_than_8 else x)

df4 = df3.drop(['price_per_sqft'], axis='columns')

dummies = pd.get_dummies(df4.Location)

df5 = pd.concat([df4,dummies],axis='columns')

df6 = df5.drop('Location', axis='columns')

X = df6.drop('Price',axis='columns')
Y = df6.Price

X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2,random_state=10)

lr_clf = LinearRegression()
lr_clf.fit(X_train.values, Y_train.values)
#score = lr_clf.score(X_test, Y_test)

#Cross val scoring
cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)

cscore = cross_val_score(LinearRegression(), X, Y, cv=cv)


#finding the best scores from different algorithms

def find_best_model_using_gridsearchcv(X,Y):
    algorithms = {
        'linear_regression' : {
            'model': LinearRegression(),
            'params': {
                'copy_X' : [True, False],
                'fit_intercept' : [True, False],
                'n_jobs' : [1,2,3],
                'positive' : [True, False]
            }
        },
        'lasso': {
            'model': Lasso(),
            'params': {
                'alpha': [1,2],
                'selection': ['random', 'cyclic']
            }
        },
        'decision_tree': {
            'model': DecisionTreeRegressor(),
            'params': {
                'criterion': ['squared_error', 'friedman_mse'],
                'splitter': ['best', 'random']
            }
        }


    }
    scores = []
    cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)
    for algo_name, config in algorithms.items():
        gs = GridSearchCV(config['model'], config['params'], cv=cv, return_train_score=False)
        gs.fit(X,Y)
        scores.append({
            'model': algo_name,
            'best_score': gs.best_score_,
            'best_params': gs.best_params_
        })

    return pd.DataFrame(scores,columns=['model','best_score','best_params'])

#bestmodelGridSearch = find_best_model_using_gridsearchcv(X,Y)

#print(bestmodelGridSearch)

def predict_price(Location, Total_Sqft, Bathroom, Bedroom):
    loc_index = np.where(X.columns==Location)[0][0]

    x = np.zeros(len(X.columns))
    x[0] = Bedroom
    x[1] = Total_Sqft
    x[2] = Bathroom
    if loc_index >= 0:
        x[loc_index] = 1


    return lr_clf.predict([x])[0]

predictedPrice = predict_price('Austin', 2000, 2, 2)


import pickle
with open('texas_home_prices_model.pickle', 'wb') as f:
    pickle.dump(lr_clf, f)

import json
columns = {
    'data_columns' : [col.lower() for col in X.columns]
}
with open("columns.json","w") as f:
    f.write(json.dumps(columns))

#print(predictedPrice)
