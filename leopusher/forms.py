from django import forms

class SendPusherChannelForm(forms.Form):
    channel_name=forms.CharField(max_length=50, required=True)
    event_name=forms.CharField(max_length=50, required=False)
    title=forms.CharField(max_length=50, required=False)
    body=forms.CharField( max_length=200, required=True)
    icon=forms.CharField( max_length=200, required=True)
    color=forms.CharField( max_length=200, required=True)
    link=forms.CharField( max_length=1100, required=True)

class SendPusherBeamForm(forms.Form):
    interests=forms.CharField( max_length=50, required=True)
    title=forms.CharField( max_length=200, required=True)
    body=forms.CharField( max_length=200, required=True)
