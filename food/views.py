from django.shortcuts import render_to_response
from food.models import Event, Review, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.forms.widgets import Input
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django import forms
from django.template.context import RequestContext
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.core.urlresolvers import reverse
from food.forms import EventCreationForm
from food.forms import RegistrationForm
from datetime import datetime
import urllib
import urllib2
import settings
import json

############################################################################################################################################
# These methods are not being used (yet) ###################################################################################################
############################################################################################################################################
def logout_user(request):
	logout(request)
	return render_to_response("index.html")

def indexview(request):
	variables = {"members" : "Rajat"}
	return render_to_response("index.html", variables)

def myFirstview(request):
	variables = {"members" : "Rajat"}
	return render_to_response("myfirst.html", variables)

#@login_required
def insertview(request):
	#we retrieve the username which will be the chef
	theUser = User.objects.get(username=request.user.username)
	
	#we retrieve all events associated to the user to pass it to the frontend
	e = Event.objects.filter(chef=theUser)

	allEvents = Event.objects.all()
	
	form = EventCreationForm()
	
	variables = {"firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id, "events" : e, "form" : form, "allEvents" : allEvents}
	return render_to_response("insert.html", variables)

############################################################################################################################################

# this class represents the email input form field for validation
class Html5EmailInput(Input):
    input_type = 'email'

# method to register a new user - first checks if the form is valid and then registers a new user
def registerNewUser(request):
	if request.method == 'POST': # If the form has been submitted...
		form = RegistrationForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			username = form.cleaned_data['username']
			firstname = form.cleaned_data['firstname']
			lastname = form.cleaned_data['lastname']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			passwordConfirmation = form.cleaned_data['passwordConfirmation']

			# we now register the user
			user = User.objects.create_user(username=username,email=email,password=password)
			profile = UserProfile.objects.create(user=user,firstName=firstname,lastName=lastname)

			return render_to_response('index.html', context_instance=RequestContext(request))
	else:
		form = RegistrationForm() # An unbound form
		return render_to_response('register.html', {'form' : form}, context_instance=RequestContext(request))
	return render_to_response('register.html', {'form' : form}, context_instance=RequestContext(request))

# method to create a new event on the dashboard
def createEvent(request):
	if request.method == 'POST':
		form = EventCreationForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			description = form.cleaned_data['description']
			date = form.cleaned_data['date']
			print date
			address = form.cleaned_data['address']
			zipCode = form.cleaned_data['zipCode']
			country = form.cleaned_data['country']
			cuisineType = form.cleaned_data['cuisineType']
			
			#we retrieve the username which will be the chef
			theUser = User.objects.get(username=request.user.username)
		
			#retrieve the coordinates of the given address
			coordinates = get_coordinates(request,address,zipCode,country)
			print coordinates

			#we retrieve all events associated to the user to pass it to the frontend
			e = Event.objects.filter(chef=theUser)

			allEvents = Event.objects.all()
			#we fill out the variables dictionary to pass it to the frontend
			variables = {"firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id, "events" : e, "form" : form, "allEvents" : allEvents}
			
			fullAddress = address + ", " + zipCode + ", " + country
			
			#we create an event and save it in the db
			if(coordinates[0] != 0 or coordinates [1] != 0):
				event = Event.objects.create(title=title, description=description, chef=theUser, creation_timestamp=datetime.now(), dateOfEvent=date, address=fullAddress, latitude=coordinates[0], longitude=coordinates[1],cuisineType=cuisineType)
				event.save()
			else:
				messages.error(request, "The address you're looking for doesn't exist! ")
				return render_to_response('insert.html', variables, context_instance=RequestContext(request))

			return render_to_response('insert.html',variables)
	else: # we create an empty form
		form = EventCreationForm()
		return form
	return form # return empty form if everything goes wrong

def viewEvent(request, event_id):
	e2 = Event.objects.get(pk=event_id)
	guests2 = e2.guests.all()
	variables = {"event" : e2, "guests" : guests2, "firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id}
	return render_to_response('viewEvent.html', variables)

def searchEvents(request):

	e1 = Event.objects.filter()
	variables = { "outputEvents" : e1, "firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id}
	return render_to_response('searchEventsResults.html',variables)

def participateInEvents(request, event_id):

	e3 = Event.objects.get(pk=event_id)
	theUser = User.objects.get(username=request.user.username)
	e3.guests.add(theUser)
	e3.save()

	guests = e3.guests.all()
	#e33 = Event.objects.filter(pk=event_id)
	variables = { "firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "event" : e3, "guests" : guests}
	return render_to_response('joinResult.html',variables)

def deleteEvent(request, event_id):
	Event.objects.filter(pk=event_id).delete()

	#we retrieve the username which will be the chef
	theUser = User.objects.get(username=request.user.username)
	# get all events associated to the user
	e = Event.objects.filter(chef=theUser)
	# create an empty form
	form = createEvent(request)
	
	allEvents = Event.objects.all()
	# fill out the variables dictionary to pass to the front end
	variables = {"firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id, "events" : e, "form" : form, "allEvents" : allEvents}
	return render_to_response('insert.html', variables)

# generic success method, not being used at all
def success(request):
	return HttpResponse('success')

# this method represents the login request
def login_user(request):
	logout(request) # logout any logged in user
	username = password = ''
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']

		#check if input username exists, or needs to be created
		num_users = User.objects.filter(username = username).count()
		if num_users == 0:
			messages.error(request, 'User ' + username + ' doesnt exist! Please register before logging in!')
		else:
			#authenticate the user
			user = authenticate(username=username, password=password)

			if user is not None:
				if user.is_active:
					# login user
					login(request, user)

					# get all events associated to the user
					e = Event.objects.filter(chef=user)

					# create an empty form
					form = createEvent(request)
					
					allEvents = Event.objects.all()
					
					print "user id" + str(request.user.id)

					# fill out the variables dictionary to pass to the front end
					variables = {"firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id, "events" : e, "form" : form, "allEvents" : allEvents}
					return render_to_response('insert.html', variables)
			else:
				messages.error(request, 'Wrong password for user ' + username)
	return render_to_response('index.html', context_instance=RequestContext(request))
	
def get_coordinates(request,address,zipCode,country):
	coordinates = (0,0)
	address = urllib.quote_plus(address)
	httpRequest = "http://maps.google.com/maps/api/geocode/json?address=" + address + "," + zipCode + "," + country
	print httpRequest
	data = urllib2.urlopen(httpRequest)
	djson = data.read()
	myData = json.loads(djson)
	print myData
	print 'before'
	if(myData['status'] == 'OK'):
		latitude = myData['results'][0]['geometry']['location']['lat']
		longitude = myData['results'][0]['geometry']['location']['lng']
		coordinates = (latitude,longitude)
		print coordinates
		return coordinates
	else:
		return coordinates