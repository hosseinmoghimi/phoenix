from django.shortcuts import render,redirect,reverse
from app.views import getContext
from .forms import *
from .repo import CreateProfiles
from django.http import JsonResponse
from app.repo import ProfileRepo
from django.views import View
from app.repo import MainPicRepo,RegionRepo
from app.enums import MainPicEnum
from app.settings import SITE_URL
TEMPLATE_ROOT='authentication/'
# Create your views here.
class AuthView(View):
    def check_available_username(self,request):
        username=request.POST['username']
        # csrfmiddlewaretoken=request.POST['csrfmiddlewaretoken']
        available=ProfileRepo(user=request.user).check_availabe_username(username=username)
        return JsonResponse({'available':available})

    def reset_password(self,request):
        user=request.user
        if request.method=='POST':
            reset_password_form=ResetPasswordForm(request.POST)
            if reset_password_form.is_valid():
                username=reset_password_form.cleaned_data['username']
                old_password=reset_password_form.cleaned_data['old_password']
                new_password=reset_password_form.cleaned_data['new_password']
                request1=ProfileRepo(user=request.user).reset_password(request=request,username=username,old_password=old_password,new_password=new_password)                
                if request1 is not None:                                     
                    return redirect(reverse('projectmanager:home'))
            
            context=getContext(request)
            context['message']='نام کاربری و کلمه عبور صحیح نمی باشد'            
            
            context['login_form']=LoginForm()
            context['register_form']=RegisterForm()
            context['reset_password_form']=ResetPasswordForm()
            context['regions']=RegionRepo(user=request.user).list()  
            
            return render(request,TEMPLATE_ROOT+'login.html',context=context)
        else:            
            return redirect(reverse('authentication:login'))
    def logout(self,request):
        ProfileRepo().logout(request)
        return redirect(reverse('authentication:login'))
    def auth(self,request,*args, **kwargs):
        
        if request.method=='POST':
            login_form=LoginForm(request.POST)
            if login_form.is_valid():
                username=login_form.cleaned_data['username']
                password=login_form.cleaned_data['password']                
                back_url=login_form.cleaned_data['back_url']
                if back_url is None or not back_url:
                    back_url=reverse('app:my_profile')                
                request1=ProfileRepo().login(request=request,username=username,password=password)
                if request1 is not None and request1.user is not None and request1.user.is_authenticated :
                    return redirect(back_url)
                else:   
                    context=getContext(request=request)         
                    context['message']='نام کاربری و کلمه عبور صحیح نمی باشد'
                    context['login_form']=LoginForm()
                    context['register_form']=RegisterForm()
                    context['back_url']=back_url
                    context['reset_password_form']=ResetPasswordForm()
                    return render(request,TEMPLATE_ROOT+'login.html',context)
        else:      
            return redirect(reverse('authentication:login'))
                
    def login(self,request,*args, **kwargs):
            context={
                'app':{
                    'logo':MainPicRepo().get(name=MainPicEnum.LOGO),
                }
            }
            if 'next' in request.GET:
                context['back_url']=request.GET['next']
            else:
                context['back_url']=reverse('app:home')
            context['login_form']=LoginForm()
            context['register_form']=RegisterForm()
            context['reset_password_form']=ResetPasswordForm()
            context['regions']=RegionRepo(user=request.user).list()               
            return render(request,TEMPLATE_ROOT+'login.html',context)
    def register(self,request):
        if request.method=='POST':
            register_form=RegisterForm(request.POST)
            if register_form.is_valid():
                region_id=register_form.cleaned_data['region_id']
                username=register_form.cleaned_data['username']
                password=register_form.cleaned_data['password']
                first_name=register_form.cleaned_data['first_name']
                last_name=register_form.cleaned_data['last_name']
                profile=ProfileRepo(user=request.user).register(username=username,password=password,first_name=first_name,last_name=last_name,region_id=region_id)                
                if profile is not None:
                    user=profile.user
                    if user is not None:
                        request1=ProfileRepo(user=request.user).login(request=request,username=user.username,password=password)
                        if request1 is not None and request1.user.is_authenticated:
                            CreateProfiles(profile=profile)
                            return redirect(reverse('app:home'))
            context=getContext(request)
            context['login_form']=LoginForm()
            context['register_form']=RegisterForm()
            context['reset_password_form']=ResetPasswordForm()
            context['regions']=RegionRepo(user=request.user).list()  
            return render(request,TEMPLATE_ROOT+'login.html',context=context)
        else:            
            return redirect(reverse('authentication:login'))



