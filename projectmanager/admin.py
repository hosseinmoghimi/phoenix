from django.contrib import admin
from .models import Employee,MaterialBrand,MaterialCategory,Material,MaterialWareHouse,MaterialObject,MaterialPackage,MaterialLog



admin.site.register(Employee)
admin.site.register(MaterialBrand)
admin.site.register(MaterialCategory)
admin.site.register(Material)
admin.site.register(MaterialWareHouse)
admin.site.register(MaterialObject)
admin.site.register(MaterialPackage)
admin.site.register(MaterialLog)