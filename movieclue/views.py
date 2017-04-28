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

        if form.is_valid():
            search_key = form.cleaned_data.get('search', '')
            choice = form.cleaned_data.get('choice', '')

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
