import os
import re
import json
import numpy as np
from sklearn import linear_model
from random import shuffle

data_dir = './data'
news_dir = './data/news'

categories = {
                'business': 1,
                'entertainment': 2,
                'politics': 3,
                'sport': 4,
                'tech': 5
        }

def get_feature_vector(contents):
    contents = {word: 1 for word in contents}
    feature_vector = []
    for category in categories:
        filename = os.path.join(data_dir, category+'.txt')
        f = open(filename)
        words = f.read().split('\n')
        for word in words:
            x = word in contents
            feature_vector.append(int(x))
    return feature_vector

def read_files():
    X = []
    Y = []
    for d in os.listdir(news_dir):
        sub_dir = os.path.join(news_dir, d)
        if os.path.isdir(sub_dir):
            for f in os.listdir(sub_dir):
                file_path = os.path.join(sub_dir, f)
                contents = open(file_path).read()
                contents = re.compile('\w+').findall(contents)
                X.append(get_feature_vector(contents))
                Y.append(categories[d])
    return X, Y

def split_dataset(X, Y):
    N = len(X)
    indices = range(N)
    shuffle(indices)
    shuffled_X = [X[index] for index in indices]
    shuffled_Y = [Y[index] for index in indices]
    X = shuffled_X[:(N * 8)/10]
    Y = shuffled_Y[:(N * 8)/10]
    X_test = shuffled_X[(N * 8)/10:]
    Y_test = shuffled_Y[(N * 8)/10:]
    return X, Y, X_test, Y_test

def classify(X, Y, X_test, Y_test):
    logreg = linear_model.LogisticRegression()
    print "Training..."
    logreg.fit(X, Y)
    print "Predicting..."
    Y_predicted = logreg.predict(X_test)
    matches = [float(Y_predicted[i]==Y_test[i]) for i in range(len(Y_test))]
    print "Accuracy = {accuracy:.2f}%".format(accuracy=100*sum(matches)/len(X_test))


X, Y = read_files()
X, Y, X_test, Y_test = split_dataset(X, Y)
classify(X, Y, X_test, Y_test)


