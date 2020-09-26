from .models import ProfileChannelEvent,PusherChannel,PusherBeam,PusherChannelEvent,PusherBeamInterest
from app.repo import ProfileRepo,NotificationRepo
class ProfileChannelEventRepo:
    def __init__(self,user):
        self.objects=ProfileChannelEvent.objects
        self.user=user
        self.profile=ProfileRepo(user=self.user).me
    def my_channel_events(self):
        return self.objects.filter(profile=self.profile)

    def get_profiles(self,channel_event_id):
        list1=self.objects.filter(channel_event_id=channel_event_id)
        profiles=[]
        for item in list1:
            profiles.append(ProfileRepo(user=self.user).get(profile_id=item.profile_id))
        
        return profiles


class PusherChannelRepo:
    def __init__(self,user=None):
        self.objects=PusherChannel.objects
    def get_by_name(self,channel_name):
        try:
            return self.objects.get(channel_name=channel_name)
        except :
            return None
    def get(self,channel_id):
        
        try:
            return self.objects.get(pk=channel_id)
        except :
            return None
    
    def list(self):
        return self.objects.all()

class PusherBeamRepo:
    def __init__(self):
        self.objects=PusherBeam.objects

    def list(self,user=None):
        return self.objects.all()

    def get(self,beam_name):
        try:
            return self.objects.get(name=beam_name)
        except :
            return None


class PusherChannelEventRepo:
     
    def add(self,channel_name,event_name):
        channel=PusherChannelRepo().get_by_name(channel_name=channel_name)
        if channel is not None:
            channel_event=self.get(channel_name=channel_name,event_name=event_name)
            if channel_event is None:            
                channel_event=channel_event(channel=channel,event_name=event_name)
                channel_event.save()
                if channel_event is not None:
                    return channel_event
    def __init__(self,user):
        self.objects=PusherChannelEvent.objects
        self.user=user
        self.profile=ProfileRepo(user=user).me
    def list_all(self):
        return self.objects.all()
      
    def add_notification_to_profiles(self,channel_event,message):
        profile_channel_event_repo=ProfileChannelEventRepo(user=self.user)
        for profile in profile_channel_event_repo.get_profiles(channel_event_id=channel_event.id):
            NotificationRepo(user=self.user).add(profile.id,title=message['title'],url=message['link'],color=message['color'],icon=message['icon'],body=message['body'])

    def get_by_names(self,channel_name,event_name):
        channel=PusherChannelRepo().get_by_name(channel_name=channel_name)
        if channel is not None:
            channel_events=self.objects.filter(channel=channel).filter(event_name=event_name)
            if len(channel_events)==1:
                return channel_events[0]

    def get(self,channel_event_id):
        try:
            channel_event=self.objects.get(pk=channel_event_id)
            return channel_event
        except :
            return None
       
    def list(self,channel_id):
        return self.objects.filter(channel_id=channel_id)
    def my_channel_events(self):
        channel_events=[]
        channel_events=self.objects.filter(id__in=ProfileChannelEvent.objects.filter(profile=self.profile).values('channel_event_id'))
        return channel_events

class PusherBeamInterestRepo:
    def add(self,beam_name,interest):
        beam=PusherBeamRepo().get(beam_name=beam_name)
        if beam is not None:
            beam_interest=self.get(beam_name=beam_name,interest=interest)
            if beam_interest is None:            
                beam_interest=PusherBeamInterest(beam=beam,interest=interest)
                beam_interest.save()
                if beam_interest is not None:
                    return beam_interest
    def __init__(self,user=None):
        self.objects=PusherBeamInterest.objects

    def list(self):
        return self.objects.all()

    def get(self,beam_name,interest):
        beam=PusherBeamRepo().get(beam_name=beam_name)
        if beam is not None:
            beam_interests=self.objects.filter(beam=beam).filter(interest=interest)
            if len(beam_interests)==1:
                return beam_interest[0]


