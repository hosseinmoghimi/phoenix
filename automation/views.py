from app import settings
from .apps import APP_NAME
from app.enums import IconsEnum, ParametersEnum
from .enums import ProductRequestStatusEnum
from .forms import *
from .repo import WorkUnitRepo,ProductRequestRepo,ProjectRepo
from app.constants import CURRENCY
from app.repo import DocumentRepo,ProfileTransactionRepo,ProfileRepo,NotificationRepo,RegionRepo
from app.serializers import NotificationSerializer
from django.shortcuts import render,redirect,reverse
from django.views import View
from django.http import Http404
from app.settings import PUSHER_IS_ENABLE
from app.views import getContext as dashboard_context

import json
TEMPLATE_ROOT='automation/'
def getContext(request):
    context=dashboard_context(request=request)
    context['APP_NAME']=APP_NAME
    return context
class BasicView(View):
    def home(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request)
        context['projects']=ProjectRepo(user=user).list()   
        return render(request,TEMPLATE_ROOT+'index.html',context)

class WorkUnitView(View):
    def add_work_unit(self,request,*args, **kwargs):
        user=request.user
        if request.method=='POST' and user and user.is_authenticated:
            add_work_unit_form=AddWorkUnitForm(request.POST)
            if add_work_unit_form.is_valid():
                project_id=add_work_unit_form.cleaned_data['project_id']      
                title=add_work_unit_form.cleaned_data['title']                
                work_unit_repo=WorkUnitRepo(user=user)
                work_unit=work_unit_repo.add(project_id=project_id,title=title)
                return redirect(reverse('automation:project',kwargs={'project_id':project_id}))
    def work_unit(self,request,work_unit_id,*args, **kwargs):
        user=request.user
        context=getContext(request)
        product_requests=ProductRequestRepo(user=request.user).list_for_work_unit(work_unit_id=work_unit_id)
        print(product_requests)
        context['product_requests']=product_requests
        context['work_unit']=WorkUnitRepo(user=user).work_unit(work_unit_id=work_unit_id)
        return render(request,TEMPLATE_ROOT+'work_unit.html',context)
class ProjectView(View):
    def project(self,request,project_id,*args, **kwargs):
        user=request.user
        context=getContext(request)
        context['project']=ProjectRepo(user=user).project(project_id=project_id)
        context['add_work_unit_form']=AddWorkUnitForm()
        return render(request,TEMPLATE_ROOT+'project.html',context)

class ProductRequestView(View):
    def list(self,request,*args, **kwargs):
        context=getContext(request=request)
        user=request.user
        if user.has_perm(APP_NAME+'.add_productrequest'):
            add_product_request_form=AddProductRequestForm()
            context['add_product_request_form']=add_product_request_form
        context['product_requests']=ProductRequestRepo(user=user).list()
        return render(request,TEMPLATE_ROOT+'product_requests.html',context)
    def product_request(self,request,product_request_id,*args, **kwargs):
        user=request.user
        context=getContext(request)
        if  True:
            context['sign_product_request_form']=SignProductRequestForm()
            context['status_options']=list(x.value for x in ProductRequestStatusEnum)
        context['product_request']=ProductRequestRepo(user=user).product_request(product_request_id=product_request_id)
        return render(request,TEMPLATE_ROOT+'product_request.html',context)
    def sign(self,request):        
        if request.method=='POST':
            sign_product_request_form=SignProductRequestForm(request.POST)
            if sign_product_request_form.is_valid():
                product_request_id=sign_product_request_form.cleaned_data['product_request_id']
                status=sign_product_request_form.cleaned_data['status']
                description=sign_product_request_form.cleaned_data['description']
                product_request=ProductRequestRepo(user=request.user).sign(status=status,product_request_id=product_request_id,description=description)
                return redirect(product_request.get_absolute_url())
                
