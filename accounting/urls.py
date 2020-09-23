from django.urls import path
from . import views
app_name='accounting'
urlpatterns = [
    path('',views.IndexView().home,name="home"),
    path('financial_year/<int:financial_year_id>/',views.IndexView().financial_year,name="financial_year"),
    path('financial_document/<int:financial_document_id>/',views.IndexView().financial_document,name="financial_document"),
    path('financial_profile/<int:financial_profile_id>/',views.IndexView().financial_profile,name="financial_profile"),
    path('financial_account/<int:financial_account_id>/',views.IndexView().financial_account,name="financial_account"),
]
