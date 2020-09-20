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


class FinancialProfileRepo:
    def __init__(self,user):
        self.user=user
        self.objects=FinancialProfile.objects
        self.profile=ProfileRepo(user=user).me
    def list(self):
        return self.objects.all()

class FinancialAccountRepo:
    def __init__(self,user):
        self.user=user
        self.objects=FinancialAccount.objects
        self.profile=ProfileRepo(user=user).me
    def list(self):
        return self.objects.all()