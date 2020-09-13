from market.models import Customer,Supplier
from django.contrib.auth import authenticate
def CreateProfiles(profile):
    Customer(profile=profile).save()
    # Supplier(profile=profile,region_id=profile.region_id).save()
    return True