from django import forms
from .models import ContactMessage


class AddCommentForm(forms.Form):
    reply_to=forms.IntegerField(required=False)
    text=forms.CharField( max_length=200, required=True)
    object_id=forms.IntegerField(required=True)
    object_type=forms.CharField(required=True,max_length=30)


class DeleteCommentForm(forms.Form):
    comment_id=forms.IntegerField(required=True)
    
class AddLikeForm(forms.Form):
    object_id=forms.IntegerField(required=True)
    object_type=forms.CharField(required=True,max_length=30)


class AddFaqForm(forms.Form):
    answer=forms.CharField(max_length=1000, required=True)
    question=forms.CharField(max_length=1000, required=True)
    priority=forms.IntegerField(required=False)
    icon=forms.CharField( max_length=30, required=True)
    color=forms.CharField( max_length=20, required=True)

class AddBlogForm(forms.Form):
    pretitle=forms.CharField(max_length=1000, required=True)
    title=forms.CharField(max_length=1000, required=True)
    icon=forms.CharField( max_length=30, required=True)
    color=forms.CharField( max_length=20, required=True)
    priority=forms.IntegerField(required=False)
    image_origin=forms.FileField(required=False)
    short_desc=forms.CharField(max_length=10000, required=True)
    description=forms.CharField(max_length=10000, required=True)    

class AddNotificationForm(forms.Form):
    title=forms.CharField(max_length=50, required=False)
    body=forms.CharField( max_length=200, required=True)
    icon=forms.CharField( max_length=200, required=True)
    color=forms.CharField( max_length=200, required=True)
    url=forms.CharField( max_length=1100, required=False)
    priority=forms.IntegerField(required=False)
    profile_id=forms.IntegerField(required=True)

class SearchForm(forms.Form):
    search_for=forms.CharField(max_length=20, required=True)

class AddLinkFrom(forms.Form):
    title=forms.CharField(max_length=200, required=True)
    url=forms.CharField(max_length=1100, required=True)
    row_number=forms.IntegerField(required=True)

class UploadProfileImageForm(forms.Form):
    profile_id=forms.IntegerField(required=True)
    image=forms.ImageField(required=True)
  
class ContactMessageForm(forms.ModelForm):    
    class Meta:
        model = ContactMessage
        fields = ("fname","lname","email","subject","message")

class EditProfileForm(forms.Form):

    profile_id=forms.IntegerField(required=True)
    first_name=forms.CharField(max_length=50, required=True)
    last_name=forms.CharField(max_length=50, required=True)
    mobile=forms.CharField(max_length=50, required=False)
    region_id=forms.CharField(max_length=50, required=False)
    address=forms.CharField(max_length=50, required=False)
    bio=forms.CharField(max_length=500, required=False)
    address=forms.CharField(max_length=100, required=False)
    postal_code=forms.CharField(max_length=50, required=False)

class ChangeProfileForm(forms.Form):
    actived=forms.IntegerField(required=True)
