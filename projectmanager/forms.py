from django import forms
class SearchForm(forms.Form):
    search_for=forms.CharField(max_length=50, required=True)