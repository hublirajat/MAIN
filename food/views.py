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
	variables = {"firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName}
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
			
			#we retrieve the username which will be the chef
			theUser = User.objects.get(username=request.user.username)
			
			#we create an event and save it in the db
			event = Event.objects.create(title=title, description=description, chef=theUser, creation_timestamp=datetime.now(), dateOfEvent=date)
			event.save()
			
			#we retrieve all events associated to the user to pass it to the frontend
			e = Event.objects.filter(chef=theUser)
			
			#we fill out the variables dictionary to pass it to the frontend
			variables = {"firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "events" : e, "form" : form}
			return render_to_response('insert.html',variables)
	else: # we create an empty form
		form = EventCreationForm()
		variables = {"firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "events" : e, "form" : form}
		return render_to_response('insert.html',variables)
	return form # return empty form if everything goes wrong

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
					
					# fill out the variables dictionary to pass to the front end
					variables = {"firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "events" : e, "form" : form}
					return render_to_response('insert.html', variables)
			else:
				messages.error(request, 'Wrong password for user ' + username)
	return render_to_response('index.html', context_instance=RequestContext(request))