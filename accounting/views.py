from django.shortcuts import render
from app.views import getContext as getAppContext
from .apps import APP_NAME
from django.views import View
from .repo import *
from app.forms import UploadProfileImageForm 
TEMPLATE_ROOT='accounting/'
def getContext(request):
    user=request.user
    context=getAppContext(request)
    context['title']='حسابداری'
    context['APP_NAME']=APP_NAME
    context['financial_profile']=FinancialProfileRepo(user=user).me
    return context


class IndexView(View):
    def home(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request)
        context['financial_year_list']=FinancialYearRepo(user=request.user).list()
        financial_profile=FinancialProfileRepo(user=user).me
        if financial_profile is not None:
            context['financial_transaction_list']=FinancialTransactionRepo(user=request.user).list_for_financial_profile(financial_profile_id=financial_profile.id)
        
        context['report']={
            'financial_reports':[
                {
                    'title':'سرمایه',
                    'amount':15000000,
                },
                {
                    'title':'بدهی',
                    'amount':890000,
                },
                {
                    'title':'دارایی',
                    'amount':4500000,
                },
            ]
        }
        return render(request,TEMPLATE_ROOT+'index.html',context)
    def financial_account_list(self,request,*args, **kwargs):
        context=getContext(request)
        context['financial_account_list']=FinancialAccountRepo(user=request.user).list()
        return render(request,TEMPLATE_ROOT+'index.html',context)
    def financial_profile(self,request,financial_profile_id,*args, **kwargs):
        context=getContext(request)
        financial_profile=FinancialProfileRepo(user=request.user).get(financial_profile_id=financial_profile_id)
        context['financial_profile']=financial_profile
        context['financial_transaction_list']=FinancialTransactionRepo(user=request.user).list_for_financial_profile(financial_profile_id=financial_profile_id)
        context['upload_profile_image_form']=UploadProfileImageForm()
        return render(request,TEMPLATE_ROOT+'financial_profile.html',context)
    def financial_account(self,request,financial_account_id,*args, **kwargs):
        context=getContext(request)
        context['financial_account']=FinancialAccountRepo(user=request.user).get(financial_account_id=financial_account_id)
        context['financial_transaction_list']=FinancialTransactionRepo(user=request.user).list_for_account(financial_account_id=financial_account_id)
        return render(request,TEMPLATE_ROOT+'index.html',context)
    def financial_year(self,request,financial_year_id,*args, **kwargs):
        context=getContext(request)
        context['financial_year']=FinancialYearRepo(user=request.user).get(financial_year_id=financial_year_id)
        context['financial_documents']=FinancialDocumentRepo(user=request.user).list_by_year(financial_year_id=financial_year_id)
        return render(request,TEMPLATE_ROOT+'financial-documents.html',context)
    def financial_document(self,request,financial_document_id,*args, **kwargs):
        context=getContext(request)
        financial_document=FinancialDocumentRepo(user=request.user).get(financial_document_id=financial_document_id)
        context['financial_document']=financial_document
        if financial_document.child_class=='financialtransaction':
            # input(ssssss)
            financial_transaction=FinancialTransactionRepo(user=request.user).get(financial_transaction_id=financial_document_id)
            context['financial_document']=financial_transaction
            context['to_account']=FinancialAccountRepo(user=request.user).get(financial_account_id=financial_transaction.to_account.pk)
            print(financial_transaction.from_account.pk)
            context['from_account']=FinancialAccountRepo(user=request.user).get(financial_account_id=financial_transaction.from_account.pk)
        # context['financial_account']=Fi
        # context['financial_documents']=FinancialDocumentRepo(user=request.user).list_by_year(financial_year_id=financial_year_id)
        return render(request,TEMPLATE_ROOT+'financial-document.html',context)
