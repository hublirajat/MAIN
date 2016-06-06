from tastypie.resources import ModelResource
from tastypie.constants import ALL
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import MultiAuthentication, BasicAuthentication, SessionAuthentication
from food.models import Event
from food.models import UserProfile

class EventResource(ModelResource):
	class Meta:
		queryset = Event.objects.all()
		resource_name = 'event'
		allowed_methods = ['get']
		filtering = {
            'user': ALL,
        }
		#authentication = MultiAuthentication(BasicAuthentication(), SessionAuthenticaton())
        #authorization = DjangoAuthorization()

class UserProfileResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'
		allowed_methods = ['get']
		#authentication = MultiAuthentication(BasicAuthentication(), SessionAuthenticaton())
        #authorization = DjangoAuthorization()
