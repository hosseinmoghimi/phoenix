from django.contrib import admin
from .models import ProfileChannelEvent,PusherChannel,PusherBeam,PusherChannelEvent,PusherBeamInterest

admin.site.register(ProfileChannelEvent)
admin.site.register(PusherChannelEvent)
admin.site.register(PusherChannel)
admin.site.register(PusherBeam)
admin.site.register(PusherBeamInterest)

    