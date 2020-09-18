from django import forms

class AddProductRequestForm(forms.Form):
    product_id=forms.IntegerField(required=True)
    quantity=forms.IntegerField(required=True)
    product_unit=forms.CharField(max_length=50, required=True)
    unit_id=forms.IntegerField(required=True)
    profile_id=forms.IntegerField(required=True)

class SignProductRequestForm(forms.Form):
    request_id=forms.IntegerField(required=True)
    status=forms.CharField(max_length=50, required=True)

class AddWorkUnitForm(forms.Form):
    project_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=50, required=True)



