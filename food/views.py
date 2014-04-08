#from django.shortcuts import render
from django.shortcuts import render_to_response
from food.models import Event, Review
from django.contrib.auth.models import User

# Create your views here.

def indexview(request):
	variables = {"members" : "Rajat"}
	return render_to_response("index.html", variables)
	
def myFirstview(request):
	variables = {"members" : "Rajat"}
	return render_to_response("myfirst.html", variables)
	
def insertview(request):
	#title = request.GET[ 'title' ]
	#description = request.GET[ 'description' ]
	variables = {"members" : "Rajat"}
	return render_to_response("insert.html", variables)