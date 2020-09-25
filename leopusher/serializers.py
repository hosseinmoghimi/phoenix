from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import PusherChannel,PusherBeam,PusherChannelEvent

class PusherChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PusherChannel
        fields = ['id', 'channel_name', 'key', 'cluster']
class PusherBeamSerializer(serializers.ModelSerializer):
    class Meta:
        model=PusherBeam
        fields=['id','name','instanse_id','interests']
    
class PusherChannelEventSerializer(serializers.ModelSerializer):
    channel=PusherChannelSerializer(read_only=True)
    class Meta:
        model=PusherChannelEvent
        fields=['id','title','channel','event_name']  
