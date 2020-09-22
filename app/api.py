from rest_framework.views import APIView
from .repo import ProfileRepo,NotificationRepo
from django.http import JsonResponse
from django.urls import path
from .constants import SUCCEED,FAILED
from .forms import *
from .repo import LikeRepo,CommentRepo
from .serializers import *
class NotificationApi(APIView):
    def add_notification(self,request):
        if not request.method=='POST':
            return JsonResponse({'result':FAILED})
        add_notification_form = AddNotificationForm(request.POST)
        if add_notification_form.is_valid():
             
            title = add_notification_form.cleaned_data['title']
            body = add_notification_form.cleaned_data['body']
            icon = add_notification_form.cleaned_data['icon']
            color = add_notification_form.cleaned_data['color']
            url = add_notification_form.cleaned_data['url']
            profile_id = add_notification_form.cleaned_data['profile_id']
            priority = add_notification_form.cleaned_data['priority']
         
            # print(new_profile['bio'])
            NotificationRepo(user=request.user).add(priority=priority,profile_id=profile_id,title=title,body=body,color=color,icon=icon,url=url) 
            return JsonResponse({'result':SUCCEED})

class BasicApi(APIView):
    def toggle_like(self,request,*args, **kwargs):
        user=request.user
        if request.method=='POST' and user and user.is_authenticated:
            add_like_form=AddLikeForm(request.POST)
            if add_like_form.is_valid():
                object_id=add_like_form.cleaned_data['object_id']
                object_type=add_like_form.cleaned_data['object_type']
                like_repo=LikeRepo(user=user,object_type=object_type)
                my_like=like_repo.toggle(object_id=object_id)
                likes_count=like_repo.count(object_id=object_id)
                return JsonResponse({'my_like':my_like,'likes_count':likes_count})

    def delete_comment(self,request,*args, **kwargs):
        user=request.user
        if request.method=='POST' and user and user.is_authenticated:
            delete_comment_form=DeleteCommentForm(request.POST)
            if delete_comment_form.is_valid():
                comment_id=delete_comment_form.cleaned_data['comment_id']                
                comment_repo=CommentRepo(user=user)
                done=comment_repo.delete(comment_id=comment_id)
                return JsonResponse({'done':done})

    def add_comment(self,request,*args, **kwargs):
        user=request.user
        if request.method=='POST' and user and user.is_authenticated:
            add_comment_form=AddCommentForm(request.POST)
            if add_comment_form.is_valid():
                object_id=add_comment_form.cleaned_data['object_id']
                object_type=add_comment_form.cleaned_data['object_type']
                text=add_comment_form.cleaned_data['text']
                
                comment_repo=CommentRepo(user=user,object_type=object_type)
                my_comment=comment_repo.add(object_id=object_id,text=text)
                comments_count=comment_repo.count(object_id=object_id)
                my_comment_s=CommentSerializer(my_comment).data
                return JsonResponse({'my_comment':my_comment_s,'comments_count':comments_count})


urlpatterns=[
    
    path('toggle_like/',BasicApi().toggle_like,name='toggle_like'),
    path('delete_comment/',BasicApi().delete_comment,name='delete_comment'),
    path('add_comment/',BasicApi().add_comment,name='add_comment'),
    
    path('add_notification/',NotificationApi().add_notification,name='add_notification'),
]


