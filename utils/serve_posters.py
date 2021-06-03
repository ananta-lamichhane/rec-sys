from omdb import OMDBClient
import os
import random


# def generate_poster_url_dict(imdb_ids):
#     """
#     generates a list of poster urls
#     :param imdb_ids: list of movie ids
#     :return: list of urls to corresponding posters.
#     """
#     client = OMDBClient(apikey=os.environ.get('OMDB_API_KEY'))
#     poster_url_list = {}
#     for imdb_id in imdb_ids:
#         data = client.get(imdbid=imdb_id)
#         poster_url_list[imdb_id] = data
#
#     return poster_url_list
def generate_movie_info(imdb_id):
    """
    generates a list of poster urls
    :param imdb_id:
    :return: list of urls to corresponding posters.
    """
    client = OMDBClient(apikey=os.environ.get('OMDB_API_KEY'))
    data = client.get(imdbid=imdb_id)
    return data


def load_next_movie(current_id):
    return current_id + 1
