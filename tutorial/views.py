from django.shortcuts import render
from .apps import APP_NAME
# Create your views here.
from app.views import getContext as AppContext
from django.views import View
TEMPLATE_ROOT='tutorial/'
def getContext(request):
    context=AppContext(request)
    context['APP_NAME']=APP_NAME
    return context

class BasicView(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request)
        context['lessons']=['a','b','c']
        return render(request,TEMPLATE_ROOT+'index.html',context)

