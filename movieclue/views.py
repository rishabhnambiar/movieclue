import requests
from django.shortcuts import render
from .forms import SearchMovieForm
import json


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

                for movie in movies:
                    url = 'http://www.omdbapi.com/?t={0}'.format(
                        movie)
                    response = requests.get(url)
                    if response.json()['Response'] == 'True':
                        context = {
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

                        contexts[movie] = context

                    # TODO: Use the above contexts to populate an HTML template
                    # with multiple results
                contexts['movies'] = movies
                print (json.dumps(contexts, indent=4, sort_keys=True))
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
            print (context)

    return render(request, 'results.html', context)
