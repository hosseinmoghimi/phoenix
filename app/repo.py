from django.contrib.auth import login, logout, authenticate
from .models import *
from .models import CountDownItem
from .enums import ParametersEnum, MainPicEnum, ProfileStatusEnum
from django.contrib.auth.models import User
from .apps import APP_NAME
from .settings import SITE_URL
from django.contrib.auth.models import Permission

from django.db.models import Avg, Max, Min,F,Q,Sum
from .constants import NOTIFICATION_UNSEEN_COUNT,NOTIFICATION_SEEN_COUNT,NOTIFICATION_ALL_COUNT


class LikeRepo:
    def __init__(self,object_type,user=None):
        if object_type=='Page':
            self.objects=Page.objects
        if self.objects is not None:
            self.user=user
            self.profile=ProfileRepo(user=user).me
    def toggle(self,object_id):
        my_like=self.my_like(object_id=object_id)
        if my_like is not None:
            my_like.delete()
            return False
        object_=self.objects.get(pk=object_id) or None
        my_like=Like.objects.create(profile=self.profile)
        my_like.save()
        object_.likes.add(my_like)

        return True
    def count(self,object_id):
        object_=self.objects.get(pk=object_id) or None
        if object_ is not None:
            try:
                my_like_count=len(object_.likes.all())
                return my_like_count
            except:
                pass
    def my_like(self,object_id):
        if self.profile is None:
            return None
        object_=self.objects.get(pk=object_id) or None
        if object_ is not None:
            try:
                my_like=object_.likes.get(profile=self.profile) or None
                if my_like is not None:
                    return my_like
            except:
                object_.likes.filter(profile=self.profile).delete()
                return None
                    

class CommentRepo:
    def __init__(self,object_type=None,user=None):
        if object_type=='Page':
            self.objects=Page.objects
        self.user=user
        self.profile=ProfileRepo(user=user).me
    def add(self,text,object_id):
        
        object_=self.objects.get(pk=object_id) or None
        my_comment=Comment.objects.create(profile=self.profile,text=text)
        my_comment.save()
        object_.comments.add(my_comment)
        return my_comment

    def delete(self,comment_id):
        try:
            comment=Comment.objects.get(pk=comment_id)
            if comment.profile==self.profile:
                comment.delete()
                return True
        except:
            pass
        return False
    def count(self,object_id):
        object_=self.objects.get(pk=object_id) or None
        if object_ is not None:
            try:
                comments_count=len(object_.comments.all())
                return comments_count
            except:
                pass
    
    
class RegionRepo():
    def __init__(self,user=None):
        self.objects=Region.objects
        self.user=user
    def list(self):
        return self.objects.all()


class TestimonialRepo:
    def __init__( self, user=None):
        self.objects=Testimonial.objects
        self.user=user   
    def list(self):
        return self.objects.order_by('priority')
    
    def list_for_home(self):
        return self.objects.filter(for_home=True).order_by('priority')


class BannerRepo:
    def __init__( self, user=None):
        self.objects=Banner.objects.filter(archive=False)
        self.user=user   
    def list(self):
        return self.objects.order_by('priority')
    
    def list_for_home(self):
        return self.objects.filter(for_home=True).order_by('priority')


class CountDownItemRepo:
    def __init__( self, user=None):
        self.objects=CountDownItem.objects
        self.user=user   
    def list(self):
        return self.objects.order_by('priority')
    
    def list_for_home(self):
        return self.objects.filter(for_home=True).order_by('priority')


class MainPicRepo:
    def __init__(self,user=None):
        self.objects=MainPic.objects
    def get(self,name):
        try:
            parameter=self.objects.get(name=name)
            return parameter
        except:
            parameter=self.objects.create(name=name,image_origin=None)
            return parameter
        
  
class MetaDataRepo:
    def __init__(self,user=None):
        self.objects=MetaData.objects
        self.user=user
    def list(self):
        return self.objects.all()
    def list_for_home(self):
        return self.objects.filter(for_home=True)


class FAQRepo:
    def __init__(self,user):
        self.user=user
        self.objects=FAQ.objects
        self.profile=ProfileRepo(user=user).me
    def add(self,question,answer,icon,color,priority):
        faq=FAQ(question=question,answer=answer,priority=priority)
        faq.save()
        return faq
    def list(self):
        return self.objects.order_by('priority')


class TagRepo:
    def __init__(self,user):
        self.user=user
        self.objects=Tag.objects
        self.profile=ProfileRepo(user=user).me
    def add(self,page_id,tag_title):
        page=PageRepo(user=self.user).page(page_id=page_id)
        if page.tags.all() and tag_title in list(tag.title for tag in page.tags.all()):
            return None
        tag=None
        try:
            tag=Tag.objects.get(title=tag_title)
        except:
            tag=Tag(title=tag_title)
            tag.save()
        if page is not None and tag is not None:
            page.tags.add(tag)
            return tag
        return tag
    def list(self):
        return self.objects.order_by('priority')
    def list_top(self):
        return self.objects.order_by('priority')[:8]
    def pages(self,tag_id):
        return Tag.objects.get(pk=tag_id).page_set.all()
    def get(self,tag_id):
        try:
            return self.objects.get(pk=tag_id)
        except:
            return None

    def tag(self,tag_id):
        return self.get(tag_id)
class ParameterRepo:
    
    def __init__(self,user=None):
        self.objects=Parameter.objects
    
    def set(self,name,value='--'):
        if value is None:
            value='--'
        self.objects.filter(name=name).delete()
        Parameter(name=name,value=value).save()
    
    def init(self,name,value=None):
        if value is None:
            value='...'
        try:
            param=self.objects.get(name=name)
        except :
            self.set(name=name,value=value)

    def get(self,name):
        try:
            parameter=self.objects.get(name=name)
        except:
            self.set(name=name)            
            parameter=self.objects.get(name=name)
        return parameter

class TechnologyRepo:
    def __init__(self,user=None):
        self.user=user
        self.objects=Technology.objects.filter(archive=False)
    def list(self):
        return self.objects.filter(archive=False).order_by('priority')
    def add(self,title,pretitle,icon,color,priority,short_desc,description):
        profile=ProfileRepo(user=self.user).me
        if self.user.has_perm(APP_NAME+'.add_blog'):
            blog=Blog(profile=profile,title=title,pretitle=pretitle,icon=icon,color=color,priority=priority,short_desc=short_desc,description=description)
            blog.save()
            if blog is not None:
                return blog
    
    def list_for_home(self):
        return self.objects.filter(for_home=True).order_by('priority')            
    def technology(self,technology_id):
        try:
            return self.objects.get(pk=technology_id)
        except:
            return None



class BlogRepo:
    def __init__(self,user=None):
        self.user=user
        self.objects=Blog.objects.filter(archive=False)
    def list(self):
        return self.objects.filter(archive=False).order_by('priority')
    def add(self,title,pretitle,icon,color,priority,short_desc,description):
        profile=ProfileRepo(user=self.user).me
        if self.user.has_perm(APP_NAME+'.add_blog'):
            blog=Blog(profile=profile,title=title,pretitle=pretitle,icon=icon,color=color,priority=priority,short_desc=short_desc,description=description)
            blog.save()
            if blog is not None:
                return blog
    
    def list_for_home(self):
        return self.objects.filter(for_home=True).order_by('priority')            
    def blog(self,blog_id):
        try:
            return self.objects.get(pk=blog_id)
        except:
            return None


class OurWorkRepo:
    def __init__(self,user=None):
        self.user=user
        self.objects=OurWork.objects.filter(archive=False)
    def list(self):
        return self.objects.filter(archive=False).order_by('priority')
          
    def our_work(self,our_work_id):
        try:
            return self.objects.get(pk=our_work_id)
        except:
            return None
    
    def get_categories(self):
        return OurWorkCategory.objects.order_by('priority')
    def list_for_home(self):
        return self.objects.filter(for_home=True).order_by('priority')


class PageRepo:
    def list_by_tag(self,tag_id):
        tag=TagRepo(user=self.user).tag(tag_id=tag_id)
        if tag is not None:
            # print(tag)
            pages= tag.page_set.all()
            # pages= self.objects.filter(tags__pk=tag_id)
            return pages
    def __init__(self,user=None):
        self.user=user
        self.objects=Page.objects.filter(archive=False)
    def list(self):
        return self.objects.filter(archive=False).order_by('priority')
          
    def page(self,page_id):
        try:
            return self.objects.get(pk=page_id)
        except:
            return None
    
    
    def list_for_home(self):
        return self.objects.filter(for_home=True).order_by('priority')

    def search(self,search_for):
        pages=self.objects.filter(title__contains=search_for)
        return pages


class NotificationRepo:

    def __init__(self,user):
        self.user=user
        self.objects=Notification.objects.order_by('-date_added')
        self.profile=ProfileRepo(user=user).me
        self.count=len(Notification.objects.filter(profile=self.profile).filter(seen=False))
    def add(self,profile_id,title,body,color,icon,url,priority=1,send_pusher=True):  
        notification=Notification(title=title,priority=priority,url=url,body=body,color=color,icon=icon,profile_id=profile_id)
        # input(profile_id)
        notification.save()
        if notification is not None:
            # PUSHER_IS_ENABLE=ParameterRepo(user=self.user).get(ParametersEnum.PUSHER_IS_ENABLE).value
            # if PUSHER_IS_ENABLE=='True':
            #     PUSHER_IS_ENABLE=True
            # else:
            #     PUSHER_IS_ENABLE=False
            # if send_pusher and PUSHER_IS_ENABLE:    
            #     channel_name=PusherChannelNameEnum.NOTIFICATION
            #     event_name=str(profile_id)
            #     if PUSHER_IS_ENABLE:
            #         notification.send(user=self.user,channel_name=channel_name,event_name=event_name)
            return notification
    def get(self,notification_id):
        profile=self.profile
        if profile is not None:
            notification=self.objects.get(pk=notification_id)
            if notification.profile==profile:
                notification.seen=True
                notification.save()
                if notification is not None:
                    return notification
    def list_seen(self):
        profile=self.profile
        if profile is not None:
            return self.objects.filter(profile=profile).filter(seen=True)[:NOTIFICATION_SEEN_COUNT]
    def list_all(self):
        profile=self.profile
        if profile is not None:
            return self.objects.filter(profile=profile)[:NOTIFICATION_ALL_COUNT]
    def list_unseen(self):
        profile=self.profile
        if profile is not None:
            return self.objects.filter(profile=profile).filter(seen=False)[:NOTIFICATION_UNSEEN_COUNT]


class SocialLinkRepo:
    def __init__(self,user=None):
        self.user=user
        self.objects=SocialLink.objects
        self.profile=ProfileRepo(user=user).me
    
    def list(self):
        return self.objects.order_by('priority')
    def list_for_home(self):
        return self.objects.filter(for_home=True).order_by('priority')


class OurServiceRepo:
    def __init__(self,user=None):
        self.objects=OurService.objects.filter(archive=False).order_by('priority')
    def list(self):
        return self.objects

    
    def list_for_home(self):
        return self.objects.filter(for_home=True).order_by('priority')


class ContactMessageRepo:
    def __init__(self,user=None):
        self.user=user
        self.objects=ContactMessage.objects
    def add(self,fname,lname,email,subject,message):
        contact_message=ContactMessage(fname=fname,lname=lname,email=email,subject=subject,message=message)
        contact_message.save()
    def list(self):
        if self.user.has_perm(APP_NAME+'.view_contactmessage'):
            return self.objects.all()


class HomeSliderRepo:
    def __init__(self,user=None):
        self.user=user
        self.objects=HomeSlider.objects.filter(archive=False)
    def list(self):
        return self.objects.order_by('priority')


class ResumeCategoryRepo:
    def __init__(self,user=None):
        self.user=user
        self.objects=ResumeCategory.objects
    def list(self,our_team_id):
        return self.objects.filter(our_team_id=our_team_id)


class GalleryPhotoRepo:    
    def __init__(self,user=None):
        self.user=user
        self.objects=GalleryPhoto.objects.filter(archive=False)
    def list(self):
        return self.objects.order_by('priority')


class OurTeamRepo:
    def __init__(self,user=None):
        self.user=user
        self.objects=OurTeam.objects
    def get_link(self):
        return ParameterRepo(user=self.user).get(ParametersEnum.OUR_TEAM_LINK)  
    def get_title(self):
        if ParameterRepo(user=self.user).get(ParametersEnum.OUR_TEAM_TITLE).value=='--':
            ParameterRepo(user=self.user).set(ParametersEnum.OUR_TEAM_TITLE,'تیم خلاق برای وب بهتر')
        return ParameterRepo(user=self.user).get(ParametersEnum.OUR_TEAM_TITLE)    
    def list(self):
        return self.objects.order_by('priority')
    
    def list_for_home(self):
        return self.objects.filter(for_home=True).order_by('priority')
    def our_team(self,our_team_id):
        try:
            return self.objects.get(pk=our_team_id)
        except:
            return None
    

class LinkRepo:
    def __init__(self,user=None):
        self.user=user
        self.profile=ProfileRepo(user=user).me
        self.objects=Link.objects.order_by('priority')
    def add(self,title,url,priority):
        link=Link(title=title,url=url,priority=priority)
        link.save()
        return link
    def delete(self,link_id,class_session_id):
        link=self.get(link_id=link_id)
        link.delete()
    def search(self,search_for):
        return self.objects.filter(Q(name__contains=search_for) | Q(link__contains=search_for))
    def get(self,link_id):
        try:
            return self.objects.get(pk=link_id)            
        except:
            return None
    def list(self):
        return self.objects.order_by('priority')
    def list_for_home(self):
        return self.objects.filter(for_home=True).order_by('priority')
    def get_nav_items(self):
        return self.objects.filter(for_nav=True).order_by('priority')



class DocumentRepo:
    def __init__(self,user=None):
        self.objects=Document.objects
        self.user=user
    def list(self):
        return self.objects.all()
    def get(self,document_id):
        try:
            return self.objects.get(pk=document_id)
        except :
            return None


class ProfileRepo:    
    def search(self,search_for):
        return self.objects.filter(Q(first_name__contains=search_for) | Q(last_name__contains=search_for))

    def __init__(self,user=None):
        if user is not None and user and user.is_authenticated:

            self.user = user
            self.objects = Profile.objects.filter(status=ProfileStatusEnum.ENABLED)
            try:
                self.me = self.objects.filter(user=user).filter(selected=True)[0]          
            except :
                profiles = self.objects.filter(user=user)
                if len(profiles)>0:
                    for profile in profiles:
                        profile.selected=False
                        profile.save()
                    profiles[0].selected=True
                    profiles[0].save()
                    self.me= profiles[0]
                else:
                    self.me=None
                    
        else:
            self.me=None
            self.objects=None
            self.user=None          
        
    def list_all(self):
        if self.user is not None and self.user.is_authenticated:
            return self.objects.all()
    
    def reset_selected_profile(self,user):
        profiles=self.objects.filter(user=user)
        if len(profiles)>0:
            for profile in profiles:
                profile.selected=False
                profile.save()
            profiles[0].selected=True
            profiles[0].save()
            return profiles[0]
        return None
  
    def get_by_user(self,user):
        if user is None or not user.is_authenticated:
            return None
        try:
            profile = self.objects.filter(user=user).filter(selected=True)[0]           
            return profile
        except :
            return self.reset_selected_profile(user=user)
    
    def list_by_user(self,user):
        profiles=self.objects.filter(user=user)
        return profiles
    
    def change_profile(self,user,actived):
        try:
            profile1=self.objects.filter(user=user).get(pk=actived)
            
            profiles=self.objects.filter(user=user)
            for profile in profiles:
                profile.selected=False
                profile.save()
            profile1.selected=True
            profile1.save()
            return profile1
        except:
            pass
        return None
    
    def change_profile_image(self,profile_id,image):
        profile=ProfileRepo(user=self.user).get(profile_id=profile_id)
        if profile is not None:
            profile.image_origin = image
            profile.save()
            return True
        return False
    
    def edit_profile(self,profile_id,first_name,last_name,mobile,region_id,address,bio,postal_code):
        user=self.user
        if user.is_authenticated:
            profile=self.get_by_user(user)
            if profile.id==profile_id or user.has_perm(APP_NAME+'.change_profile'):
                edited_profile=self.objects.get(pk=profile_id)
                
                if edited_profile is not None:
                    edited_profile.first_name=first_name
                    edited_profile.last_name=last_name
                    edited_profile.mobile=mobile
                    edited_profile.region_id=region_id
                    edited_profile.bio=bio
                    edited_profile.address=address
                    edited_profile.postal_code=postal_code
                    
                    edited_profile.save()
                    return edited_profile
        return None
    
    def reset_password(self,request,username,new_password,old_password=None):
        user=self.user
        try:
            selected_user=User.objects.get(username=username)
        except:
            selected_user=None
        
        if selected_user is not None :            
            if self.user is not None and self.user.is_authenticated and self.user.has_perm(APP_NAME+'.change_profile'):                                    
                selected_user.set_password(new_password)
                selected_user.save()
                if selected_user is not None:
                    return True
            selected_user=authenticate(request=request,username=username,password=old_password)                                    
            if selected_user is not None:
                    selected_user.set_password(new_password)
                    selected_user.save()
                    if selected_user is not None:
                        request=self.login(request=request,username=username,password=new_password)
                        return request
                               
    def get(self,profile_id):
        user=self.user
        try:

            profile=self.objects.get(pk=profile_id)
            return profile
        except:
            return None
        
        current_profile=self.get_by_user(user)
        if current_profile is None:
            return None
        if user.has_perm('app.view_profile'):
            profile=self.objects.filter(pk=profile_id)
            if len(profile)==1:
                return profile[0]
        if current_profile.id==profile_id:
            return current_profile
    
    def check_availabe_username(self,username):

        return False if len(User.objects.filter(username=username))>0 else True
    
    def register(self,username,password,first_name,last_name,region_id):
        if not self.check_availabe_username(username):
            return None
        user = User.objects.create_user(username=username,email= 'new_user@khafonline.com', password=password)

        # Update fields and then save again
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        profile=Profile(user=user,first_name=first_name,mobile='',last_name=last_name,region_id=region_id)
        profile.save()
        return profile

    def login(self,request,username,password):
        user=authenticate(request=request,username=username,password=password)
        if user is not None:
            login(request,user)
            if user.is_authenticated:                
                return request  
        return None
    
    def logout(self,request):
        logout(request=request)

    def my_permissions(self):
        user=self.user
        if user.is_superuser:
            return Permission.objects.all()
        return user.user_permissions.all() | Permission.objects.filter(group__user=user)


class ProfileTransactionRepo:
    def __init__(self,user=None):
        self.objects=ProfileTransaction.objects.order_by('-date_added')
        self.user=user        
        self.profile=ProfileRepo(user=self.user).me
    
    def rest(self,profile_id=None,until_date=None,transaction_id=None):  
      
        if self.profile is not None and profile_id is None:
            profile_id=ProfileRepo(user=self.user).me.id
        transactions=ProfileTransaction.objects         
        transactions_to=transactions.filter(to_profile_id=profile_id)#.aggregate(Sum('amount'))
        transactions_from=transactions.filter(from_profile_id=profile_id)#.aggregate(Sum('amount'))
        if transaction_id is not None:
                transactions=transactions.filter(id__lte=transaction_id)      
            
        if until_date is not None:
                transactions=transactions.filter(date_added__lte=until_date)
        
        
        if len(transactions_to)==0:
            transactions_to={'sum':0}
        else:
            transactions_to=transactions_to.aggregate(sum=Sum('amount'))
        
        if len(transactions_from)==0:
            transactions_from={'sum':0}
        else:
            transactions_from=transactions_from.aggregate(sum=Sum('amount'))
        
        rest=transactions_from['sum']-transactions_to['sum']
        return rest

    def add(self,from_profile_id,to_profile_id,title,amount,cash_type,description):
        transaction=ProfileTransaction(
            from_profile_id=from_profile_id,
            to_profile_id=to_profile_id,
            title=title,
            amount=amount,
            cash_type=cash_type,
            description=description
        )

        transaction.save()
        return transaction
    

    def list(self,profile_id=None,until_date=None,transaction_id=None):
        transactions=self.objects
        if self.profile is not None and profile_id is None:
            profile_id=self.profile.id
        if self.profile is not None:
            transactions=transactions.filter(Q(from_profile_id=profile_id) | Q(to_profile_id=profile_id))
            if transaction_id is not None:
                transactions=transactions.filter(id__lte=transaction_id)      
            
            if until_date is not None:
                transactions=transactions.filter(date_added__lte=until_date)
            
            for transaction in transactions:
                transaction.rest=transaction.rest(profile_id=profile_id)
                transaction.direction=transaction.direction(profile_id)
            return transactions      


class SignatureRepo:
    def __init__(self,user):
        self.objects=Signature.objects
        self.user=user
        self.profile=ProfileRepo(user=self.user).me
    def add(self,description,status):
        if self.profile is not None:
            signature=Signature(profile=self.profile,status=status,description=description)
            signature.save()
            return signature
