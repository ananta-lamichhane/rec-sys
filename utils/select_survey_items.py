import os
import pandas as pd
def select_movies_for_survey():
    """

    :param param1: select movies using some criteria (e.g. age, prefernce, etc.)
    :param param2:
    :param param3:
    :return: a list of ids of movies

    Right now selects 10 random movies from dataset

    """
    filename = os.path.realpath('./database/datasets/movielens_small/links.csv')

    df = pd.read_csv(filename, usecols=['imdbId'], dtype=str) ## direct import deletes leading zeros str is must.
    df = df.sample(n=10).to_numpy().flatten().tolist() ## change to list of strings
    movielist = ["tt" + movie for movie in df]

    return movielist