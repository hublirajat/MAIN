from tastypie.resources import ModelResource
from tastypie.constants import ALL
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import MultiAuthentication, BasicAuthentication, SessionAuthentication
from food.models import Event
from food.models import UserProfile
from django.contrib.auth.models import User


class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
        allowed_methods = ['get']
        resource_name = 'event'

class UserProfileResource(ModelResource):
	class Meta:
		queryset = UserProfile.objects.all()
		resource_name = 'userprofile'
        allowed_methods = ['get']
        filtering = { "firstName" : ALL }

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        allowed_methods = ['get']
