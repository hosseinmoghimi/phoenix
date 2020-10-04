

from django.contrib import admin
from .models import Contractor,MaterialInStock,Assignment,Image,Issue,MaterialRequest,PageLog,ProjectCategory,Project,WorkUnit,Employee,MaterialBrand,MaterialCategory,Material,MaterialWareHouse,MaterialObject,MaterialPackage,MaterialLog
from app.repo import ProfileRepo
from .enums import LogActionEnum
class MaterialRequestAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        user=request.user
        profile=ProfileRepo(user=user).me
        log=PageLog(page=obj,manager_page_id=obj.pk,name=obj.title,profile=profile,action=LogActionEnum.SAVE)
        log.save()
class ProjectAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.location:
            obj.location=obj.location.replace('width="600"','width="100%"')
            obj.location=obj.location.replace('height="450"','height="400"')
        super().save_model(request, obj, form, change)
        user=request.user
        profile=ProfileRepo(user=user).me
        log=PageLog(page=obj,manager_page_id=obj.pk,name=obj.title,profile=profile,action=LogActionEnum.SAVE)
        log.save()


    def delete_model(self, request, obj):
        user=request.user
        profile=ProfileRepo(user=user).me
        log=PageLog(page=obj,manager_page_id=obj.pk,name=obj.title,profile=profile,action=LogActionEnum.DELETE)
        log.save()
        super().delete_model(request, obj)
class AssignmentAdmin(admin.ModelAdmin):
    list_display=('assign_to','title','date_added')
admin.site.register(MaterialRequest,MaterialRequestAdmin)
admin.site.register(Assignment,AssignmentAdmin)
admin.site.register(Issue)
admin.site.register(MaterialInStock)
admin.site.register(Image)
admin.site.register(Contractor)
admin.site.register(PageLog)
admin.site.register(ProjectCategory)
admin.site.register(Project,ProjectAdmin)
admin.site.register(WorkUnit)
admin.site.register(Employee)
admin.site.register(MaterialBrand)
admin.site.register(MaterialCategory)
admin.site.register(Material)
admin.site.register(MaterialWareHouse)
admin.site.register(MaterialObject)
admin.site.register(MaterialPackage)
admin.site.register(MaterialLog)