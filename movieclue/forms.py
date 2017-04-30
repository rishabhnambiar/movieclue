from django import forms


class SearchMovieForm(forms.Form):
    search = forms.CharField(label='', max_length=25, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    choices = [('movie', 'MOVIES'),
               ('series', 'TV')]

    choice = forms.ChoiceField(label='', choices=choices, widget=forms.Select(
        attrs={'class': 'dropdown'}))
