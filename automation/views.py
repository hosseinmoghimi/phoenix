from app import settings
from .apps import APP_NAME
from app.enums import IconsEnum, ParametersEnum
from .forms import *
from .repo import WorkUnitRepo,ProductRequestRepo
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
    return context
class BasicView(View):
    def home(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request)
        context['work_units']=WorkUnitRepo(user=user).list()
        context['product_requests']=ProductRequestRepo(user=user).list()        
        return render(request,TEMPLATE_ROOT+'index.html',context)
class WorkUnitView(View):
    def work_unit(self,request,work_unit_id,*args, **kwargs):
        user=request.user
        context=getContext(request)
        context['work_unit']=UnitRepo(user=user).unit(work_unit_id=work_unit_id)
        return render(request,TEMPLATE_ROOT+'work_unit.html',context)

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
        context['product_request']=ProductRequestRepo(user=user).product_request(product_request_id=product_request_id)
        return render(request,TEMPLATE_ROOT+'product_request.html',context)