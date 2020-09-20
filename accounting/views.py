from django.shortcuts import render
from app.views import getContext as getAppContext
from .apps import APP_NAME
from django.views import View
from .repo import *
TEMPLATE_ROOT='accounting/'
def getContext(request):
    context=getAppContext(request)
    context['title']='حسابداری'
    return context


class IndexView(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request)
        context['financial_year_list']=FinancialYearRepo(user=request.user).list()
        return render(request,TEMPLATE_ROOT+'index.html',context)
    def financial_account_list(self,request,*args, **kwargs):
        context=getContext(request)
        context['financial_account_list']=FinancialAccountRepo(user=request.user).list()
        return render(request,TEMPLATE_ROOT+'index.html',context)
    def financial_profile(self,request,financial_profile_id,*args, **kwargs):
        context=getContext(request)
        context['financial_transaction_list']=FinancialTransactionRepo(user=request.user).list_for_financial_profile(financial_profile_id=financial_profile_id)
        return render(request,TEMPLATE_ROOT+'index.html',context)
    def financial_account(self,request,financial_account_id,*args, **kwargs):
        context=getContext(request)
        context['financial_account']=FinancialAccountRepo(user=request.user).get(financial_account_id=financial_account_id)
        context['financial_transaction_list']=FinancialTransactionRepo(user=request.user).list_for_account(financial_account_id=financial_account_id)
        return render(request,TEMPLATE_ROOT+'index.html',context)
    def financial_year(self,request,financial_year_id,*args, **kwargs):
        context=getContext(request)
        context['financial_year']=FinancialYearRepo(user=request.user).get(financial_year_id=financial_year_id)
        context['financial_documents']=FinancialDocumentRepo(user=request.user).list_by_year(financial_year_id=financial_year_id)
        return render(request,TEMPLATE_ROOT+'index.html',context)
    def financial_document(self,request,financial_document_id,*args, **kwargs):
        context=getContext(request)
        context['financial_document']=FinancialDocumentRepo(user=request.user).get(financial_document_id=financial_document_id)
        # context['financial_documents']=FinancialDocumentRepo(user=request.user).list_by_year(financial_year_id=financial_year_id)
        return render(request,TEMPLATE_ROOT+'index.html',context)
