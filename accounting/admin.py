from django.contrib import admin
from .models import *

admin.site.register(FinancialDocumentCategory)
admin.site.register(FinancialYear)
admin.site.register(FinancialAccount)
admin.site.register(FinancialTransaction)
admin.site.register(FinancialProfile)
admin.site.register(FinancialDocument)
admin.site.register(Cash)
admin.site.register(BankAccount)
admin.site.register(Bank)
admin.site.register(CurrentFeeCategory)
admin.site.register(CurrentFee)

