from tastypie.resources import ModelResource
from food.models import Event

class EventResource(ModelResource):
	class Meta:
		queryset = Event.objects.all()
		resource_name = 'event'
