from django.contrib import admin
from .models import Agent,ProductRequestSignature,WorkUnit,ProductRequest,PurchaseAgent,LetterSignature,Letter,Project

admin.site.register(WorkUnit)
admin.site.register(Agent)
admin.site.register(LetterSignature)
admin.site.register(ProductRequestSignature)
admin.site.register(ProductRequest)
admin.site.register(PurchaseAgent)
admin.site.register(Letter)
admin.site.register(Project)
