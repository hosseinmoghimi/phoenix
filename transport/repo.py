from .models import RequestService
from app.repo import ProfileRepo
class RequestServiceRepo:
    def __init__(self,user):
        self.user=user
        self.profile=ProfileRepo(user=user).me
        self.objects=RequestService.objects
    def list(self):
        return self.objects.all()