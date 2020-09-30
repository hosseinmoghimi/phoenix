
from django.contrib import admin
from django.urls import path,include
from . import views
app_name="app"
urlpatterns = [
    path('',views.BasicView().home,name='home'),
    path('api/',include('app.api')),
    path('my_profile/',views.ProfileView().profile,name='my_profile'),
    path('profile/<int:profile_id>/',views.ProfileView().profile,name='profile'),
    path('transactions/<int:profile_id>/',views.TransactionView().transactions,name='transactions'),    
    path('about/',views.BasicView().about,name='about'),
    path('terms/',views.BasicView().terms,name='terms'),
    path('add_tag/',views.PageView().add_tag,name='add_tag'),
    path('faq/',views.BasicView().faq,name='faq'),
    path('tag/<int:tag_id>/',views.PageView().tag,name='tag'),
    path('blogs/',views.PageView().blogs,name='blogs'),
    path('page/<int:page_id>/',views.PageView().page,name='page'),
    path('add_blog/',views.PageView().add_blog,name='add_blog'),
    path('blog/<int:blog_id>/',views.PageView().blog,name='blog'),
    path('our_works/',views.PageView().our_works,name='our_works'),
    path('our_work/<int:our_work_id>/',views.PageView().our_work,name='our_work'),
    path('our_team/<int:our_team_id>/',views.BasicView().our_team,name='our_team'),
    path('resume/<int:our_team_id>/',views.BasicView().resume,name='resume'),
    path('change_profile_image/',views.ProfileView().change_profile_image,name='change_profile_image'),
    path('edit_profile/',views.ProfileView().edit_profile,name='edit_profile'),
    path('change_profile/',views.ProfileView().change_profile,name='change_profile'),
    path('search/',views.BasicView().search,name='search'),
    path('manager/',views.ManagerView().manager,name='manager'),
    path('contact/',views.ContactView.as_view(),name='contact'),
    path('notifications/',views.BasicView().notifications,name='notifications'),
    path('notification/<int:notification_id>/',views.BasicView().notifications,name='notification'),
    path('download/<int:document_id>/',views.BasicView().download,name='download'),
    path('technology/<int:technology_id>/',views.PageView().technology,name='technology'),
    
]
