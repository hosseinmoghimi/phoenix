from django import forms
from app.constants import *

class DeleteProductCommentForm(forms.Form):
    comment_id=forms.IntegerField(required=True)


class AddProductCommentForm(forms.Form):
    product_id=forms.IntegerField(required=True)
    comment=forms.CharField( max_length=200, required=True)

class DeleteProductForm(forms.Form):
    product_id=forms.IntegerField(required=True)
    parent_id=forms.IntegerField(required=True)

class EditProductForm(forms.Form):
    name=forms.CharField( max_length=100, required=True)
    unit_name=forms.CharField( max_length=50, required=False)
    image=forms.ImageField(required=False,widget=forms.ClearableFileInput(attrs={'class':'btn btn-warning','v-model':'upload-profile','multiple': False}))
    
    short_description=forms.CharField(max_length=500, required=False)
    description=forms.CharField( max_length=5000, required=False)
    def __init__(self, *args, **kwargs):
        super(EditProductForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'accept': 'image/*'})
    
class AddToMyFavoritesForm(forms.Form):
    product_id=forms.IntegerField(required=False)

class RemoveFromMyFavoritesForm(forms.Form):
    product_id=forms.IntegerField(required=False)

class SearchForm(forms.Form):
    search_for=forms.CharField(max_length=50,required=True)

class RemoveShopForm(forms.Form):
    shop_id=forms.IntegerField(required=True)

class SubmitCartForm(forms.Form):
    supplier_id=forms.IntegerField(required=False)
    customer_id=forms.IntegerField(required=False)
    address=forms.CharField( max_length=200, required=True)
    description=forms.CharField( max_length=200, required=False)
    no_ship=forms.BooleanField(required=False)

class CheckoutForm(forms.Form):
    address=forms.CharField( max_length=200, required=True)
    description=forms.CharField( max_length=200, required=False)

class DoDeliverForm(forms.Form):
    order_id=forms.IntegerField(required=True)
    description=forms.CharField( max_length=100, required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'توضیحات'}))

class DoShipForm(forms.Form):
    order_id=forms.IntegerField(required=True)
    description=forms.CharField( max_length=100, required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'توضیحات'}))

class DoPackForm(forms.Form):
    order_id=forms.IntegerField(required=True)
    count_of_packs=forms.IntegerField( required=False,widget=forms.TextInput(attrs={'class':'form-control','type':'number','placeholder':'تعداد پاکت'}))
    description=forms.CharField(  max_length=100,required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'توضیحات'}))

class CancelOrderForm(forms.Form):
    order_id=forms.IntegerField(required=True)    
    description=forms.CharField(  max_length=100,required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'توضیحات'}))

class ConfirmOrderForm(forms.Form):
    order_id=forms.IntegerField(required=True)    
    description=forms.CharField(  max_length=100,required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'توضیحات'}))

class DeleteAddressForm(forms.Form):
    address_id=forms.IntegerField(required=True)

class EditProfileForm(forms.Form):
    first_name=forms.CharField(max_length=50, required=True)
    last_name=forms.CharField(max_length=50, required=True)
    #mobile=forms.CharField(max_length=11, required=True)
    #email=forms.EmailField(required=False)
    bio=forms.CharField( max_length=200, required=False)
    region=forms.CharField(max_length=50, required=False)

class AddCategoryForm(forms.Form):
    parent_id=forms.IntegerField(required=False)
    name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'دسته بندی جدید'}), max_length=50, required=True)  

class AddProductForm(forms.Form):
    unit_name=forms.CharField(max_length=50, required=False)
    category_id=forms.IntegerField(required=True)
    name=forms.CharField(max_length=50,required=True)  
    
class AddShopForm(forms.Form):
    supplier_id=forms.IntegerField(required=True)  
    product_id=forms.IntegerField( required=True)  
    unit_name=forms.CharField(required=True)  
    available=forms.IntegerField(required=False)  
    price=forms.IntegerField(required=True)  
    
class AddToCartForm(forms.Form):
    customer_id=forms.IntegerField(required=False)
    shop_id=forms.IntegerField(required=True)
    quantity=forms.IntegerField(required=False)

class RemoveFromCartForm(forms.Form):
    shop_id=forms.IntegerField(required=True)

class AddAddressForm(forms.Form):
    city=forms.CharField(max_length=50, required=True)
    street=forms.CharField(max_length=100, required=True)
    agent=forms.CharField(max_length=50, required=True)
    tel=forms.CharField(max_length=50, required=True)
    title=forms.CharField(max_length=50, required=True)

class AddProductLikeForm(forms.Form):
    product_id=forms.IntegerField(required=True)
class RegisterForm(forms.Form):
    region=forms.CharField(max_length=20,required=True)
    username=forms.CharField(max_length=50, required=True)
    password=forms.CharField(max_length=150, required=True)
    first_name=forms.CharField(max_length=50, required=True)
    last_name=forms.CharField(max_length=50, required=True)