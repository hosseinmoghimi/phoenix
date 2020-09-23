from django.shortcuts import render,redirect,reverse

from django.views import View
from django.http import Http404
from app.views import getContext as AppContext
from .apps import APP_NAME
TEMPLATE_ROOT='projectmanager/'
def getContext(request):
    context=AppContext(request)
    return context
class BasicView(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request)
        return render(request,TEMPLATE_ROOT+'index.html',context)

