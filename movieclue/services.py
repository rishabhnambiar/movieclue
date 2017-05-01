import requests


def find_a_movie(form):

    if form.is_valid():
        search_key = form.cleaned_data.get('search', '')
        choice = form.cleaned_data.get('choice', '')

    # The requests package will generate a request with the required data:
    # The URL looks like :
    # https://www.omdbapi.com/?t=Firefly&type=series

    url = 'http://www.omdbapi.com/?t={0}&type={1}'.format(
        search_key, choice)
    response = requests.get(url)

    # Checking for API failure
    if response.status_code == requests.codes.ok:

        # If movie was found in OMDb
        if response.json()['Response'] == 'True':

            movie_details = {
                'title': response.json()['Title'],
                'genre': response.json()['Genre'],
                'release': response.json()['Released'],
                'plot': response.json()['Plot'],
                'rating': response.json()['imdbRating'],
                'poster_url': response.json()['Poster'],
                'year': response.json()['Year'],
                'runtime': response.json()['Runtime'],
                'errorstatus': False,
            }

        else:
            # Retrieving error message
            movie_details = {
                'error': response.json()['Error'],
                'errorstatus': True,
            }

    return movie_details


def find_many_movies(form):

    desired_movies = list()
    if form.is_valid():
        search_key = form.cleaned_data.get('search', '')
        choice = form.cleaned_data.get('choice', '')

    movies = search_key.split('+')

    # URL generated for every movie in desired_movies (list)
    # Details of for every movie stored in movie_details (dict)

    for movie in movies:
        url = 'http://www.omdbapi.com/?t={0}&type={1}'.format(
            movie, choice)
        response = requests.get(url)

        if response.status_code == requests.codes.ok:
            if response.json()['Response'] == 'True':

                movie_details = {
                    'year': response.json()['Year'],
                    'poster_url': response.json()['Poster'],
                    'runtime': response.json()['Runtime'],
                    'title': response.json()['Title'],
                    'genre': response.json()['Genre'],
                    'plot': response.json()['Plot'],
                    'errorstatus': False,
                    'rating': response.json()['imdbRating'],
                    'release': response.json()['Released'],
                }

            else:
                movie_details = {
                    'error': response.json()['Error'],
                    'errorstatus': True,
                }
            desired_movies.append(movie_details)

    return desired_movies
