from django.shortcuts import render
from app.views import getContext as dashboardContext
from django.views import View
from .repo import RequestServiceRepo
TEMPLATE_ROOT='transport/'
def getContext(request):
    context=dashboardContext(request=request)
    return context

class IndexView(View):
    def home(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request=request)
        context['request_services']=RequestServiceRepo(user=user).list()
        return render(request,TEMPLATE_ROOT+'index.html',context)