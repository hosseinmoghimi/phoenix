from django.shortcuts import render
from app.views import getContext as getAppContext
from .apps import APP_NAME
from django.views import View
from .repo import FinancialTransactionRepo,FinancialProfileRepo,FinancialAccountRepo
TEMPLATE_ROOT='accounting/'
def getContext(request):
    context=getAppContext(request)
    context['title']='حسابداری'
    return context


class IndexView(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request)
        context['financial_account_list']=FinancialAccountRepo(user=request.user).list()
        return render(request,TEMPLATE_ROOT+'index.html',context)
    def financial_profile(self,request,financial_profile_id,*args, **kwargs):
        context=getContext(request)
        context['financial_transaction_list']=FinancialTransactionRepo(user=request.user).list_for_financial_profile(financial_profile_id=financial_profile_id)
        return render(request,TEMPLATE_ROOT+'index.html',context)
    def financial_account(self,request,financial_account_id,*args, **kwargs):
        context=getContext(request)
        context['financial_transaction_list']=FinancialTransactionRepo(user=request.user).list_for_account(financial_account_id=financial_account_id)
        return render(request,TEMPLATE_ROOT+'index.html',context)
