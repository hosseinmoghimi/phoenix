from rest_framework import serializers
from .models import Comment,Blog,Profile,Link,Notification


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model=Blog
        fields=['id','pretitle','icon','color','title','short_desc','description','image','persian_date_added','get_absolute_url']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['id','text','profile_id','profile_name','date_added','profile_image']
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['id','name','image','get_absolute_url']      

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model=Link
        fields=['id','title','url','row_number']      

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notification
        fields=['id','title','url','get_absolute_url','icon','body','seen','date_added','color']