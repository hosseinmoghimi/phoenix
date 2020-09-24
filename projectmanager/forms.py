from django import forms
class SearchForm(forms.Form):
    search_for=forms.CharField(max_length=50, required=True)
    

class PriorityForm(forms.Form):
    pk=forms.CharField(max_length=50, required=True)
    direction=forms.CharField(max_length=5, required=True)
    base_class=forms.CharField(max_length=20,required=True)