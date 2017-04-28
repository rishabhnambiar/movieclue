import requests
from django.shortcuts import render
from .forms import SearchMovieForm


def home(request):
    form = SearchMovieForm()
    context = {
        "form": form
    }
    return render(request, 'search.html', context)


def find(request):
    if request.method == 'GET':
        form = SearchMovieForm(request.GET)
        contexts = {}

        if form.is_valid():
            search_key = form.cleaned_data.get('search', '')
            choice = form.cleaned_data.get('choice', '')

            if ',' in search_key:
                movies = search_key.split(',')
                print (movies)
                for movie in movies:
                    url = 'http://www.omdbapi.com/?t={0}'.format(
                        movie)
                    response = requests.get(url)
                    if response.json()['Response'] == 'True':
                        contexts[movie] = [
                            response.json()['Year'],
                            response.json()['Poster'],
                            response.json()['Runtime'],
                            response.json()['Title'],
                            response.json()['Genre'],
                            response.json()['Plot'],
                            response.json()['Response'],
                            response.json()['imdbRating'],
                            response.json()['Released'],
                        ]

                    context = {
                        'year': contexts[movie][0],
                        'poster_url': contexts[movie][1],
                        'runtime': contexts[movie][2],
                        'title': contexts[movie][3],
                        'genre': contexts[movie][4],
                        'plot': contexts[movie][5],
                        'errorstatus': False,
                        'rating': contexts[movie][7],
                        'release': contexts[movie][8],
                    }
                    print(context)
                    # TODO: Use the above contexts to populate an HTML template
                    # with multiple results

                return render(request, 'results.html', contexts)

            url = 'http://www.omdbapi.com/?t={0}&type={1}'.format(
                search_key, choice)
            response = requests.get(url)

            if response.json()['Response'] == 'True':
                context = {
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
                context = {
                    'error': response.json()['Error'],
                    'errorstatus': True,
                }

    return render(request, 'results.html', context)
