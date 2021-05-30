# -*- coding: utf-8 -*-
"""
Created on Fri May 28 11:11:43 2021

@author: Amine
"""

from surprise import KNNBaseline
from surprise import CoClustering
from surprise import SVD
from surprise import Reader
from surprise import Dataset

from collections import defaultdict
from operator import itemgetter
import heapq

import os
import csv

# load the movie ratings and return

def load_dataset():
    ratings_dataset = 0
    
    # specify the columns order to read the data correctly
    reader= Reader(line_format='user item rating timestamp', sep=',', skip_lines=1) 
    ratings_dataset= Dataset.load_from_file('ml-latest-small/ratings.csv', reader=reader)
    
    # link movie movie's name with its ID 
    movieID_to_Name={}
    with open('ml-latest-small/movies.csv', newline='', encoding='ISO-8859-1')as csvfile:
        movie_reader=csv.reader(csvfile)
        next(movie_reader)
        for row in movie_reader:
            movieID= int(row[0])
            movie_name= row[1]
            movieID_to_Name[movieID]= movie_name
    #return both the dataset and the linked movie Id to name in tuple
    return (ratings_dataset, movieID_to_Name)

dataset, movieID_to_Name= load_dataset()

#print(dataset, movieID_to_Name)

# from movie id get the movie name
def getMovieName(movieID):
    if int(movieID) in movieID_to_Name:
        return movieID_to_Name[int(movieID)]
    else:
        return ""

# buil a full surprise training set from dataset
trainset= dataset.build_full_trainset()

# use cosine similarity to estimate ratings

sim_options = {'name': 'cosine',
               'user_based': False  # compute  similarities between items
               }
similarity_matrix = KNNBaseline(sim_options=sim_options).fit(trainset).compute_similarities()

# pick a random user ID, has to be a numerical string
#see how final recommendations change
# depending on the user 1-610
test_subject= '500'

#Get thr top K items user rated
k=20

# Convert raw ids (string and integers) to inned ids as a unique integer
#so Surprise could manipulate them 
test_subject_iid= trainset.to_inner_uid(test_subject)


#get the top K items our user rated (sorted)
test_subject_ratings = trainset.ur[test_subject_iid]
k_neighbors = heapq.nlargest(k, test_subject_ratings, key=lambda t: t[1])


#Defaultdict when trying to access a key that does not exist it creates a new entry with that key, no error
candidates = defaultdict(float)

for itemID , rating in k_neighbors:
    try:
        similarities = similarity_matrix[itemID]
        for innerID, score in enumerate(similarities):
            candidates[innerID]+= score * (rating/5.0)
    except:
        continue


# Build a dictionary of movies the user has watched
# trainset.ur[test_subject_iid] are items rated by the specific user
watched={}
for itemID, rating in trainset.ur[test_subject_iid]:
    watched[itemID]= 1

# add not watched movies and similar to his favorite movies to recommendation list
recommendations =[]

position = 0
for itemID, rating_sum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
    if not itemID in watched:
        recommendations.append(getMovieName(trainset.to_raw_iid(itemID)))
        position +=1
        if(position >10): break # only top 10 movies to recommend

for rec in recommendations:
    print("Movie:", rec)
    
    
    
    
    
    














