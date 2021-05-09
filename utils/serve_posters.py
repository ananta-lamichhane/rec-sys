from omdb import OMDBClient
import os

def generate_poster_url_dict(imdb_ids):
    """
    :param imdb_ids: list of movie ids
    :return: list of urls to corresponding posters.
    """
    client = OMDBClient(apikey=os.environ.get('OMDB_API_KEY'))
    poster_url_list = []
    for imdb_id in imdb_ids:
        data = client.get(imdbid=imdb_id)
        poster_url = data['poster']
        print(poster_url)
        poster_url_list.append(poster_url)

    return poster_url_list
