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
        contexts = list()

        if form.is_valid():
            search_key = form.cleaned_data.get('search', '')
            choice = form.cleaned_data.get('choice', '')

            # For multiple movie search using '+' as a delimiter
            if '+' in search_key:
                movies = search_key.split('+')

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
                    else:
                        context = {
                            'error': response.json()['Error'],
                            'errorstatus': True,
                        }

                    # Accumulating details of all movies in contexts (list)
                    contexts.append(context)

                return render(request, 'results.html', {'movies': contexts})

            # For single movie search
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

    return render(request, 'result.html', context)
