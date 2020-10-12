from django.shortcuts import render
from .apps import APP_NAME
# Create your views here.
from app.views import getContext as AppContext
from django.views import View
from .repo import LessonRepo
from app.repo import TagRepo,LikeRepo
from app.forms import AddLikeForm,AddCommentForm,DeleteCommentForm
import json
from app.serializers import CommentSerializer,TagSerializer

TEMPLATE_ROOT='tutorial/'
def getContext(request):
    context=AppContext(request)
    context['APP_NAME']=APP_NAME
    return context

class BasicView(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request)
        context['lessons']=LessonRepo(user=request.user).list()
        
        return render(request,TEMPLATE_ROOT+'index.html',context)
    def lesson(self,request,lesson_id,*args, **kwargs):
        
        context=getContext(request)
        page=LessonRepo(user=request.user).lesson(lesson_id)
        context['page']=page
        page_id=lesson_id
        if page is None:
            raise Http404
        tags=TagRepo(user=request.user).list_top()
        context['tags']=tags
        context['add_like_form']=AddLikeForm()
        context['get_edit_url']=page.get_edit_url()
        context['add_comment_form']=AddCommentForm()
        context['delete_comment_form']=DeleteCommentForm()
        comments_s=json.dumps(CommentSerializer(page.comments,many=True).data)
        context['comments_s']=comments_s
        context['my_like']=LikeRepo(user=request.user,object_type='Page').my_like(object_id=page_id)
        
        return render(request,'avo/page.html',context)

