from django import forms
from django.shortcuts import reverse
from .apps import APP_NAME
from app.settings import SITE_URL
class AddMaterialRequestForm(forms.Form):
    material_id=forms.IntegerField(required=True)
    quantity=forms.IntegerField(required=True)
    unit_name=forms.CharField(max_length=50, required=True)
    project_id=forms.IntegerField(required=True)

class SearchForm(forms.Form):
    action=f'{SITE_URL}{APP_NAME}/search/'
    search_for=forms.CharField(max_length=50, required=True)
    

class AddIssueForm(forms.Form):
    issue_for_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=50,required=True)
    issue_type=forms.CharField(max_length=50,required=True)
    

class SignMaterialRequestForm(forms.Form):
    material_request_id=forms.IntegerField(required=True)
    status=forms.CharField(max_length=50, required=True)
    description=forms.CharField(max_length=500, required=False)

class PriorityForm(forms.Form):
    pk=forms.CharField(max_length=50, required=True)
    direction=forms.CharField(max_length=5, required=True)
    base_class=forms.CharField(max_length=20,required=True)