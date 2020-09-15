from app import settings
from .apps import APP_NAME
from .enums import IconsEnum, ParametersEnum,MainPicEnum
from app.forms import *
from authentication.forms import *
from app.constants import CURRENCY,SUCCEED,FAILED
from .repo import LikeRepo,PageRepo,TagRepo,BannerRepo,TestimonialRepo,OurWorkRepo,MainPicRepo,ContactMessageRepo,SocialLinkRepo,BlogRepo,FAQRepo,OurServiceRepo,ResumeCategoryRepo,OurTeamRepo,HomeSliderRepo,DocumentRepo, ParameterRepo, LinkRepo, MetaDataRepo, OurTeamRepo, RegionRepo, NotificationRepo
from app.serializers import NotificationSerializer,BlogSerializer,CommentSerializer
from app.repo import ProfileTransactionRepo,ProfileRepo
from django.shortcuts import render,redirect,reverse
from django.views import View
from django.http import Http404,JsonResponse
from app.settings import PUSHER_IS_ENABLE,STATIC_URL,MEDIA_URL
import json

if PUSHER_IS_ENABLE:
    from leopusher.repo import PusherChannelEventRepo
    from leopusher.serializers import PusherChannelEventSerializer
    PusherChannelEventRepo


TEMPLATE_ROOT='constructioncompany/'
TEMPLATE_ROOT_DASHBOARD='dashboard/'


def getContext(request):
    user=request.user
    context={}
    context['TEMPLATE_ROOT']=TEMPLATE_ROOT
    context['CURRENCY']=CURRENCY 
    
    context['links']=LinkRepo(user=user).list_for_home()
    context['social_links']=SocialLinkRepo().list_for_home() 
    if user.is_authenticated:
        profile=ProfileRepo(user=user).me    
        context['profile']=profile 
        context['notifications_s']=json.dumps(NotificationSerializer(NotificationRepo(user=request.user).list_unseen(),many=True).data)
        context['notifications_count']=NotificationRepo(user=user).count
        profiles=ProfileRepo(user=user).list_by_user(user=user)
        if profile is not None:
            context['profiles']=profiles.exclude(pk=profile.pk)
        if PUSHER_IS_ENABLE:            
            my_channel_events=PusherChannelEventRepo(user=user).my_channel_events()
            my_channel_events_s=PusherChannelEventSerializer(my_channel_events,many=True).data
            context['my_channel_events_s']=json.dumps(my_channel_events_s)
    else:
        context['profile']=None                
        context['profiles']=None            
        context['my_channel_events_s']='[]'
        context['notifications_s']='[]'

    parameter_repo=ParameterRepo(user=user)
    context['theme_color']=parameter_repo.get(ParametersEnum.THEME_COLOR).value
    context['PUSHER_IS_ENABLE']=PUSHER_IS_ENABLE
    context['engapp']={
        'slogan':parameter_repo.get(ParametersEnum.SLOGAN),
        'logo':MainPicRepo().get(name=MainPicEnum.LOGO),
        'pretitle':parameter_repo.get(ParametersEnum.PRE_TILTE),
        'title':parameter_repo.get(ParametersEnum.TITLE),
        'address':parameter_repo.get(ParametersEnum.ADDRESS),    
        'mobile':parameter_repo.get(ParametersEnum.MOBILE),           
        'email':parameter_repo.get(ParametersEnum.EMAIL),      
        'tel':parameter_repo.get(ParametersEnum.TEL),
        'url':parameter_repo.get(ParametersEnum.URL),
        'meta_data_items':MetaDataRepo().list_for_home(),
        'our_team_title':OurTeamRepo(user=user).get_title(),
        'our_team_link':OurTeamRepo(user=user).get_link(),
    }
    context['SITE_URL']=settings.SITE_URL
    context['MEDIA_URL']=settings.MEDIA_URL
    context['ADMIN_URL']=settings.ADMIN_URL
    context['APP_NAME']=APP_NAME
    context['DEBUG']=settings.DEBUG
    
    # context['current_profile']=ProfileRepo.get_by_user()

    #leoData
    context['search_form']=SearchForm()
    return context


def csrf_failure(request, reason=""):
        context=getContext(request=request)
        context['message']=ParameterRepo(user=request.user).get(ParametersEnum.CSRF_FAILURE_MESSAGE).value        
        context['login_form']=LoginForm()
        context['register_form']=RegisterForm()
        return render(request,TEMPLATE_ROOT+'login.html',context)


class BlogView(View):
    def add_blog(self,request,*args, **kwargs):
        if request.method=='POST':
            add_blog_form=AddBlogForm(request.POST,request.FILES)
            if add_blog_form.is_valid():  
                image=''
                title=add_blog_form.cleaned_data['title']
                pretitle=add_blog_form.cleaned_data['pretitle']
                icon=add_blog_form.cleaned_data['icon']
                color=add_blog_form.cleaned_data['color']
                priority=add_blog_form.cleaned_data['priority']
                short_desc=add_blog_form.cleaned_data['short_desc']
                description=add_blog_form.cleaned_data['description']
     
                blog=BlogRepo(user=request.user).add(title=title,
                pretitle=pretitle,icon=icon,color=color,priority=priority,short_desc=short_desc,description=description)
                if blog is not None:
                    return JsonResponse({'result':SUCCEED,'blog':BlogSerializer(blog).data}) 
            return JsonResponse({'result':FAILED})
    def list(self,request,page=1,*args, **kwargs):
        user=request.user
        main_pic_repo=MainPicRepo(user=user)

        context=getContext(request=request)
        context['blog_header_image']=main_pic_repo.get(name=MainPicEnum.BLOG_HEADER)
        if user.has_perm(APP_NAME+'.add_blog'):
            context['add_blog_form']=AddBlogForm()
            icons=list(IconsEnum)
            context['icons_s']=json.dumps(icons)
        context['blogs']=BlogRepo(user=request.user).list()
        return render(request,TEMPLATE_ROOT+'blogs.html',context)
    def blog(self,request,blog_id,*args, **kwargs):
        context=getContext(request=request)
        page=BlogRepo(user=request.user).blog(blog_id=blog_id)
        context['page']=page
        page_id=blog_id
        if page is None:
            raise Http404
        tags=TagRepo(user=request.user).list_top()
        context['tags']=tags
        context['add_like_form']=AddLikeForm()
        context['get_edit_url']=page.get_edit_url()
        context['add_comment_form']=AddCommentForm()
        context['delete_comment_form']=DeleteCommentForm()
        comments_s=json.dumps(CommentSerializer(page.comments,many=True).data)
        context['comments_s']=comments_s
        context['my_like']=LikeRepo(user=request.user,object_type='Page').my_like(object_id=page_id)
        return render(request,TEMPLATE_ROOT+'page.html',context)
    def page(self,request,page_id,*args, **kwargs):
        context=getContext(request=request)
        page=PageRepo(user=request.user).page(page_id=page_id)
        
        context['page']=page
        page_id=page_id
        if page is None:
            raise Http404
        tags=TagRepo(user=request.user).list_top()
        context['tags']=tags
        context['add_like_form']=AddLikeForm()
        context['get_edit_url']=page.get_edit_url()
        context['add_comment_form']=AddCommentForm()
        context['delete_comment_form']=DeleteCommentForm()
        comments_s=json.dumps(CommentSerializer(page.comments,many=True).data)
        context['comments_s']=comments_s
        context['my_like']=LikeRepo(user=request.user,object_type='Page').my_like(object_id=page_id)
        return render(request,TEMPLATE_ROOT+'page.html',context)
    def tag(self,request,tag_id,*args, **kwargs):
        user=request.user
        main_pic_repo=MainPicRepo(user=user)

        context=getContext(request=request)
        context['blog_header_image']=main_pic_repo.get(name=MainPicEnum.BLOG_HEADER)
        if user.has_perm(APP_NAME+'.add_blog'):
            context['add_blog_form']=AddBlogForm()
            icons=list(IconsEnum)
            context['icons_s']=json.dumps(icons)
        context['pages_pre_title']=f'Tag '
        tag=TagRepo(user=user).get(tag_id=tag_id)        
        context['pages_title']=tag.title
        if tag.image_header :
            context['pages_header_image']=tag
        else:
            context['pages_header_image']=main_pic_repo.get(name=MainPicEnum.TAG_HEADER)

        
        context['pages']=TagRepo(user=request.user).pages(tag_id=tag_id)
        return render(request,TEMPLATE_ROOT+'pages.html',context)

class OurWorkView(View):
    def add_blog(self,request,*args, **kwargs):
        if request.method=='POST':
            add_blog_form=AddBlogForm(request.POST,request.FILES)
            if add_blog_form.is_valid():  
                image=''
                title=add_blog_form.cleaned_data['title']
                pretitle=add_blog_form.cleaned_data['pretitle']
                icon=add_blog_form.cleaned_data['icon']
                color=add_blog_form.cleaned_data['color']
                priority=add_blog_form.cleaned_data['priority']
                short_desc=add_blog_form.cleaned_data['short_desc']
                description=add_blog_form.cleaned_data['description']
     
                blog=BlogRepo(user=request.user).add(title=title,
                pretitle=pretitle,icon=icon,color=color,priority=priority,short_desc=short_desc,description=description)
                if blog is not None:
                    return JsonResponse({'result':SUCCEED,'blog':BlogSerializer(blog).data}) 
            return JsonResponse({'result':FAILED})
    def list(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request=request)
        if user.has_perm(APP_NAME+'.add_blog'):
            context['add_blog_form']=AddBlogForm()
            icons=list(IconsEnum)
            context['icons_s']=json.dumps(icons)
        context['our_works_header_image']=MainPicRepo(user=request.user).get(name=MainPicEnum.OUR_WORK_HEADER)        
        context['our_works']=OurWorkRepo(user=request.user).list()
        return render(request,TEMPLATE_ROOT+'our_works.html',context)
    def our_work(self,request,our_work_id,*args, **kwargs):
        context=getContext(request=request)
        page=OurWorkRepo(user=request.user).our_work(our_work_id=our_work_id)
        
        context['page']=page
        page_id=our_work_id
        if page is None:
            raise Http404
        tags=TagRepo(user=request.user).list_top()
        context['tags']=tags
        context['location']={'value':page.location}
        context['add_like_form']=AddLikeForm()
        context['get_edit_url']=page.get_edit_url()
        context['add_comment_form']=AddCommentForm()
        context['delete_comment_form']=DeleteCommentForm()
        comments_s=json.dumps(CommentSerializer(page.comments,many=True).data)
        context['comments_s']=comments_s
        context['my_like']=LikeRepo(user=request.user,object_type='Page').my_like(object_id=page_id)
        return render(request,TEMPLATE_ROOT+'page.html',context)


class BasicView(View):
    def download(self,request,document_id):
        download=DocumentRepo(user=request.user).get(document_id=document_id).download()
        return download
    def notifications(self,request,notification_id=None):
        user=request.user
        context=getContext(request=request)
        if notification_id is None:
            
            notifications_seen=NotificationRepo(user=user).list_seen()
            notifications_unseen=NotificationRepo(user=user).list_unseen()
            # for notification in notifications_seen:
            #     if notification.seen:
            #         notification.color='scecondary'
            context['notifications_seen']=notifications_seen
            context['notifications_unseen']=notifications_unseen
        else:
            context['notification']=NotificationRepo(user=user).get(notification_id=notification_id)
        context['notifications_s']=json.dumps(NotificationSerializer(NotificationRepo(user=request.user).list_unseen(),many=True).data)
        return render(request,TEMPLATE_ROOT_DASHBOARD+'notifications.html',context)
    def about(self,request,*args, **kwargs):  
        user=request.user     
        main_pic_repo=MainPicRepo(user=request.user)
        parameter_repo=ParameterRepo(user=request.user)
        context=getContext(request=request)
        context['our_teams']=OurTeamRepo(user=request.user).list()
        context['our_services']=OurServiceRepo(user=user).list()
        context['testimonials']=TestimonialRepo(user=request.user).list()
        context['banners']=BannerRepo(user=request.user).list()
        context['about_us_short']=parameter_repo.get(ParametersEnum.ABOUT_US_SHORT)
        
        about_header_image=main_pic_repo.get(MainPicEnum.ABOUT_HEADER)
        context['about_header_image']=about_header_image
        about_pic=main_pic_repo.get(MainPicEnum.ABOUT)
        context['about_pic']=about_pic
        context['about_us_title']=parameter_repo.get(ParametersEnum.ABOUT_US_TITLE)
        context['about_us']=ParameterRepo(user=request.user).get(ParametersEnum.ABOUT_US)
        return render(request,TEMPLATE_ROOT+'about.html',context)
    def terms(self,request):        
        context=getContext(request=request)
        context['terms']=ParameterRepo(user=request.user).get(ParametersEnum.TERMS)
        return render(request,TEMPLATE_ROOT_DASHBOARD+'terms.html',context)
    def faq(self,request):
        if request.method=='POST':
            add_faq_form=AddFaqForm(request.POST)
            if add_faq_form.is_valid():
                question=add_faq_form.cleaned_data['question']
                answer=add_faq_form.cleaned_data['answer']
                icon=add_faq_form.cleaned_data['icon']
                color=add_faq_form.cleaned_data['color']
                priority=add_faq_form.cleaned_data['priority']
                faq=FAQRepo(user=request.user).add(question=question,answer=answer,icon=icon,color=color,priority=priority)
                if faq is not None:
                    return redirect(reverse('app:faq'))
                
        else:
            
            user=request.user
            context=getContext(request=request)
            if user.has_perm(APP_NAME+'.add_faq'):
                context['add_faq_form']=AddFaqForm()
            context['faqs']=FAQRepo(user=request.user).list()
            return render(request,TEMPLATE_ROOT_DASHBOARD+'faq.html',context)
    def our_team(self,request):        
        context=getContext(request=request)
        context['our_teams']=OurTeamRepo(user=request.user).list()
        return render(request,TEMPLATE_ROOT_DASHBOARD+'our_team.html',context)
    def resume(self,request,our_team_id):        
        context=getContext(request=request)
        context['resume_categories']=ResumeCategoryRepo(user=request.user).list(our_team_id=our_team_id)
        return render(request,TEMPLATE_ROOT_DASHBOARD+'resume.html',context)
    def search(self,request):
        if request.method=='POST':
            search_form=SearchForm(request.POST)
            if search_form.is_valid():
                search_for=search_form.cleaned_data['search_for']          
                context=getContext(request=request)
                context['pages_pre_title']=f'جست و جو برای '
                context['pages_title']=search_for
                context['pages_header_image']=MainPicRepo().get(name=MainPicEnum.SEARCH)
                context['blogs']=PageRepo(user=request.user).search(search_for=search_for)           
                return render(request,TEMPLATE_ROOT+'pages.html',context)

    def home(self,request):
        user=request.user
        parameter_repo=ParameterRepo(user=user)
        context=getContext(request=request)        
        context['home_sliders']=HomeSliderRepo(user=user).list()
        context['our_services']=OurServiceRepo(user=user).list_for_home()
        context['about_us_title']=parameter_repo.get(ParametersEnum.ABOUT_US_TITLE)
        context['about_us_short']=parameter_repo.get(ParametersEnum.ABOUT_US_SHORT)
        
        context['blogs']=BlogRepo(user=request.user).list_for_home()
        context['our_works']=OurWorkRepo(user=request.user).list_for_home()
        context['testimonials']=TestimonialRepo(user=request.user).list_for_home()
        context['banners']=BannerRepo(user=request.user).list_for_home()
        about_pic=MainPicRepo(user=request.user).get(MainPicEnum.ABOUT)
        if about_pic is not None:
            context['about_pic']=about_pic
        return render(request,TEMPLATE_ROOT+'index.html',context)


class ContactView(View):
    def get(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request=request)
        parameter_repo=ParameterRepo()
        main_pic_repo=MainPicRepo(user=request.user)
        context['contact_header_image']=main_pic_repo.get(name=MainPicEnum.CONTACT_HEADER)
        context['email']=parameter_repo.get(ParametersEnum.EMAIL)
        context['address']=parameter_repo.get(ParametersEnum.ADDRESS)
        context['tel']=parameter_repo.get(ParametersEnum.TEL)
        context['mobile']=parameter_repo.get(ParametersEnum.MOBILE)
        context['fax']=parameter_repo.get(ParametersEnum.FAX)
        context['location']=parameter_repo.get(ParametersEnum.LOCATION)
        context['contact_us']=parameter_repo.get(ParametersEnum.CONTACT_US)
        context['contact_form']=ContactMessageForm()
        return render(request,TEMPLATE_ROOT+'contact.html',context)
    def post(self,request,*args, **kwargs):
        if request.method=='POST':
            contact_form=ContactMessageForm(request.POST)
            if contact_form.is_valid():
                fname=contact_form.cleaned_data['fname']
                lname=contact_form.cleaned_data['lname']
                email=contact_form.cleaned_data['email']
                subject=contact_form.cleaned_data['subject']
                message=contact_form.cleaned_data['message']
                ContactMessageRepo().add(fname=fname,lname=lname,email=email,subject=subject,message=message)
                return redirect(reverse('app:contact'))


class ProfileView(View):
    
    def change_profile_image(self,request):
        upload_profile_image_form=UploadProfileImageForm(request.POST,request.FILES)
        if upload_profile_image_form.is_valid():
            image=request.FILES['image']
            profile_id=upload_profile_image_form.cleaned_data['profile_id']
            ProfileRepo(user=request.user).change_profile_image(profile_id=profile_id,image=image)                    
            return redirect(reverse('app:profile',kwargs={'profile_id':profile_id}))
    def edit_profile(self,request):
        if not request.method=='POST':
            return redirect('app:home')
        edit_profile_form=EditProfileForm(request.POST)
        if edit_profile_form.is_valid():
            
            profile_id=edit_profile_form.cleaned_data['profile_id']
            first_name=edit_profile_form.cleaned_data['first_name']
            last_name=edit_profile_form.cleaned_data['last_name']
            region_id=edit_profile_form.cleaned_data['region_id']
            mobile=edit_profile_form.cleaned_data['mobile']
            address=edit_profile_form.cleaned_data['address']
            bio=edit_profile_form.cleaned_data['bio']
            # print(new_profile['bio'])
            profile=ProfileRepo(user=request.user).edit_profile(profile_id=profile_id,first_name=first_name,last_name=last_name,mobile=mobile,region_id=region_id,address=address,bio=bio) 
        return redirect(reverse('app:profile',kwargs={'profile_id':profile.pk}))
    def change_profile(self,request):
        if not request.method=='POST':
            return redirect('app:home')
        change_profile_form=ChangeProfileForm(request.POST)
        if change_profile_form.is_valid():
            actived=change_profile_form.cleaned_data['actived']
            profile=ProfileRepo(user=request.user).change_profile(user=request.user,actived=actived) 
        return redirect(reverse('app:home'))
        

    def profile(self,request,profile_id=0):
        user=request.user
        context=getContext(request=request)
        if not user.is_authenticated:
            return redirect(reverse("authentication:login"))
        active_profile=ProfileRepo(user=user).me
    
        selected_profile=ProfileRepo(user=user).get(profile_id=profile_id)
        if selected_profile is None:                
            raise Http404
        context['selected_profile']=selected_profile
        if (selected_profile is not None and selected_profile.user==request.user) or request.user.has_perm(f'{APP_NAME}.change_profile'):
            context['regions']=RegionRepo(user=user).list().exclude(pk=selected_profile.region_id)
            context['edit_profile_form']=EditProfileForm()
            context['upload_profile_image_form']=UploadProfileImageForm() 
            

        if selected_profile.user==request.user or request.user.has_perm(f'{APP_NAME}.view_profiletransaction'):
            transaction_repo=ProfileTransactionRepo(user=user)
            transactions=transaction_repo.list(profile_id=profile_id)[:20]                
            context['transactions']=transactions
            context['rest']=transaction_repo.rest(profile_id=profile_id)
        
        return render(request,TEMPLATE_ROOT_DASHBOARD+'profile.html',context)


class TransactionView(View):
    def transactions(self,request,profile_id,*args, **kwargs):
        user=request.user
        profile=ProfileRepo(user=user).get(profile_id=profile_id)
        context=getContext(request=request)
        transaction_repo=ProfileTransactionRepo(user=user)
        transactions=transaction_repo.list(profile_id=profile_id)
        context['transactions']=transactions
        context['transaction_title']=profile.name
        context['rest_all']=transaction_repo.rest(profile_id=profile_id)
        return render(request,TEMPLATE_ROOT_DASHBOARD+'transactions.html',context)


class ManagerView(View):
    
    def manager(self,request):
        user=request.user
        if user is None or not user.is_authenticated:
            return BasicView().home(request)
        context=getContext(request=request)
        priority_range=range(6)
        context['priority_range']=priority_range
        site_profiles=ProfileRepo(user=user).list_all()
        icons=list(IconsEnum)
        context['icons_s']=json.dumps(icons)
        context['site_profiles']=site_profiles
        if user.has_perm('app.add_notification'):
            add_notification_form=AddNotificationForm()
            context['add_notification_form']=add_notification_form
            return render(request,TEMPLATE_ROOT_DASHBOARD+'manager.html',context)
        return BasicView().home(request)