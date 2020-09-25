from django.views import View
from django.shortcuts import render,redirect,reverse
from .repo import PusherChannelEventRepo,PusherChannelRepo,ProfileChannelEventRepo

from app.views import getContext as dashboardContext 
from .forms import *
from django.http import JsonResponse
from app.enums import IconsEnum
from .serializers import PusherChannelEventSerializer
import json

TEMPLATE_ROOT='pusher/'
def getContext(request):
    context = dashboardContext(request=request)
    context["title"] = 'pusher'
    
    return context

class BeamView(View):
    def send_beam(self,request):
        if request.method=='POST':
            send_pusher_beam_form=SendPusherBeamForm(request.POST)
            if send_pusher_beam_form.is_valid():
                interests=send_pusher_beam_form.cleaned_data['interests']
                title=send_pusher_beam_form.cleaned_data['title']
                body=send_pusher_beam_form.cleaned_data['body']    
                # response=MyPusherBeam(user=request.user).send_beam(interests=interests,title=title,body=body)                          
                return redirect(reverse('dashboard:manager'))
    def get(self,request):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+'beam.html',context)

class IndexView(View):
    def channels(self,request,channel_id=None,channel_event_id=None):
        user=request.user
        context=getContext(request=request)
        if channel_id is not None:
            channels=[].append(PusherChannelRepo(user=user).get(channel_id=channel_id))
            channel_events=PusherChannelEventRepo(user=user).list(channel_id=channel_id)
            context['channels']=channels
            context['channel_events']=channel_events
        elif channel_event_id is not None:
            channel_event=PusherChannelEventRepo(user=user).get(channel_event_id=channel_event_id)
            channel_events=[].append(channel_event)
            context['channel_events']=channel_events
            profiles=ProfileChannelEventRepo(user=user).get_profiles(channel_event_id=channel_event_id)
            context['profiles']=profiles
        else:
            channels=PusherChannelRepo(user=user).list()
            context['channels']=channels
            print(channels)

        return render(request,TEMPLATE_ROOT+'list.html',context)
    def get(self,request):
        context=getContext(request=request)
        icons=list(IconsEnum)
        context['icons_s']=json.dumps(icons)
            
        context["send_pusher_beam_form"] = SendPusherBeamForm()
        context["send_pusher_channel_form"] = SendPusherChannelForm()
        channel_events=PusherChannelEventRepo(user=request.user).list_all()
        context['channel_events']=channel_events
        context['channel_events_s']=json.dumps(PusherChannelEventSerializer(channel_events,many=True).data)
        return render(request,TEMPLATE_ROOT+'pusher.html',context)
class ChannelView(View):
    def send_channel(self,request):        
        if request.method=='POST':
            send_pusher_channel_form=SendPusherChannelForm(request.POST)
            if send_pusher_channel_form.is_valid():
                title=send_pusher_channel_form.cleaned_data['title']       
                body=send_pusher_channel_form.cleaned_data['body']        
                icon=send_pusher_channel_form.cleaned_data['icon']        
                color=send_pusher_channel_form.cleaned_data['color']       
                event_name=send_pusher_channel_form.cleaned_data['event_name']       
                channel_name=send_pusher_channel_form.cleaned_data['channel_name']   
                link=send_pusher_channel_form.cleaned_data['link']           
       
                data={}
                # MyPusherChannel(user=request.user).send(channel_name=channel_name,event_name=event_name,title=title,message=message,data=data)#.submit(order_id=order.id,total=order.total(),supplier_id=order.supplier.id)
                
                channel_event=PusherChannelEventRepo().get_by_names(channel_name=channel_name,event_name=event_name)
                
                if channel_event is not None:
                    channel_event.send_message(message={
                        'title': title,
                        'body': body,
                        'color': color,
                        'icon': icon,
                        'link': link,
                        })
                    return JsonResponse({'result':'SUCCESS'})
 
    def get(self,request):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+'pusher.html',context)