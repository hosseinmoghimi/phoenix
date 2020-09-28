from django.shortcuts import render
from .apps import APP_NAME
# Create your views here.
from app.views import getContext as AppContext
from django.views import View
from .repo import LessonRepo

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
        context['page']=LessonRepo(user=request.user).lesson(lesson_id)
        
        return render(request,'avo/page.html',context)

