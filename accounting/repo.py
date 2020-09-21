from .models import *
from app.repo import ProfileRepo
from django.db.models import Q


class FinancialTransactionRepo:
    def __init__(self,user):
        self.user=user
        self.objects=FinancialTransaction.objects
        self.profile=ProfileRepo(user=user).me
    def list_for_financial_profile(self,financial_profile_id):
        profile=FinancialProfile.objects.get(pk=financial_profile_id)
        return self.objects.filter(Q(from_account=profile)|Q(to_account=profile))
    def list_for_profile(self,profile_id):
        profile=ProfileRepo(user=self.user).get(profile_id=profile_id)
        profile=FinancialProfile.objects.get(profile=profile)
        return self.objects.filter(Q(from_account=profile)|Q(to_account=profile))

    def list_for_account(self,financial_account_id):
        return self.objects.filter(Q(from_account_id=financial_account_id)|Q(to_account_id=financial_account_id))

    def get(self,financial_transaction_id):
        try:
            return self.objects.get(pk=financial_transaction_id)
        except:
            return None

class FinancialProfileRepo:
    def __init__(self,user):
        self.user=user
        self.objects=FinancialProfile.objects
        self.profile=ProfileRepo(user=user).me
        try:
            self.me=self.objects.get(profile=self.profile)
        except:
            self.me=None
    def list(self):
        return self.objects.all()

    def get(self,financial_profile_id):
        try:
            return self.objects.get(pk=financial_profile_id)
        except:
            return None

class FinancialAccountRepo:
    def __init__(self,user):
        self.user=user
        self.objects=FinancialAccount.objects
        self.profile=ProfileRepo(user=user).me
    def get(self,financial_account_id):
        try:
            return FinancialProfile.objects.get(pk=financial_account_id)
        except:
            pass

        try:
            return self.objects.get(pk=financial_account_id)
        except:
            return None
    def list(self):
        return self.objects.all()


class FinancialYearRepo:
    def __init__(self,user):
        self.user=user
        self.objects=FinancialYear.objects
        self.profile=ProfileRepo(user=user).me
    def get(self,financial_year_id):
        try:
            return self.objects.get(pk=financial_year_id)
        except:
            return None
    def list(self):
        return self.objects.all()


class FinancialDocumentRepo:
    def __init__(self,user):
        self.user=user
        self.objects=FinancialDocument.objects
        self.profile=ProfileRepo(user=user).me
    def get(self,financial_document_id):
        try:
            return self.objects.get(pk=financial_document_id)
        except:
            return None
    def list(self):
        return self.objects.all()
    def list_by_year(self,financial_year_id):
        return self.objects.filter(financial_year_id=financial_year_id)