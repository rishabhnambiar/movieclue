from django.shortcuts import render
from .forms import SearchMovieForm
from movieclue.services import *


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

        # For a single movie/series search
        if '+' not in search_key:
            movie_details = find_a_movie(form)
            return render(request, 'result.html', movie_details)

        # For multiple movie/series search using '+' as a delimiter
        else:
            desired_movies = find_many_movies(form)
            return render(request, 'results.html', {'movies': desired_movies})
