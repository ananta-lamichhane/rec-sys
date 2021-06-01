from omdb import OMDBClient
import os
import random


def generate_poster_url_dict(imdb_ids):
    """
    generates a list of poster urls
    :param imdb_ids: list of movie ids
    :return: list of urls to corresponding posters.
    """
    client = OMDBClient(apikey=os.environ.get('OMDB_API_KEY'))
    if type(imdb_ids) is list:
        poster_url_list = []
        for imdb_id in imdb_ids:
            data = client.get(imdbid=imdb_id)
            new_data = {}
            new_data['poster_url'] = data['poster']
            new_data['name'] = data['title']
            new_data['imdb_id'] = imdb_id
            poster_url_list.append(new_data)
            #poster_url_list['image_url'] = poster_url

        return poster_url_list
    else:
        data = client.get(imdbid=imdb_ids)
        return data
