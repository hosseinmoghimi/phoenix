from rest_framework.views import APIView
from authentication.forms import LoginForm
from django.http import JsonResponse
from app.constants import SUCCEED,FAILED
from app.repo import ProfileRepo,NotificationRepo
from app.serializers import *
from app.forms import AddNotificationForm
