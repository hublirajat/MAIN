from django.shortcuts import render_to_response
from food.models import Event, Review, UserProfile, Notify
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
from food.forms import ReviewForm
from food.forms import RegistrationForm
from datetime import datetime
import urllib
import urllib2
import settings
import json
from django.db.models import Q

############################################################################################################################################
# These methods are not being used (yet) ###################################################################################################
############################################################################################################################################
def logout_user(request):
	logout(request)
	return render_to_response("index.html")

#@login_required
def insertview(request):
	#we retrieve the username which will be the chef
	theUser = User.objects.get(username=request.user.username)

	# get all events associated to the user
	e1 = Event.objects.filter(chef=theUser).order_by('dateOfEvent')
	e2 = Event.objects.filter(guests=theUser).order_by('dateOfEvent')
	e3 = e2 | e1
	e = e3.distinct()

	allEvents = Event.objects.all()

	form = EventCreationForm()
	
	notifications = Notify.objects.filter(user=request.user)

	variables = {"firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id, "events" : e, "form" : form, "allEvents" : allEvents, "notifications" : notifications}
	
	return render_to_response("insert.html", variables)

############################################################################################################################################

# this class represents the email input form field for validation
class Html5EmailInput(Input):
    input_type = 'email'

# method to register a new user - first checks if the form is valid and then registers a new user
def registerNewUser(request):
	if request.method == 'POST': # If the form has been submitted...
		form = RegistrationForm(request.POST,request.FILES) # A form bound to the POST data
		print form.errors
		if form.is_valid(): # All validation rules pass
			username = form.cleaned_data['username']
			firstname = form.cleaned_data['firstname']
			lastname = form.cleaned_data['lastname']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			passwordConfirmation = form.cleaned_data['passwordConfirmation']
			gender = form.cleaned_data['gender']
			profilePicture = form.cleaned_data['profilePicture']
			address = form.cleaned_data['address']
			zipCode = form.cleaned_data['zipCode']
			country = form.cleaned_data['country']

			# we now register the user
			user = User.objects.create_user(username=username,email=email,password=password)
			profile = UserProfile.objects.create(user=user,firstName=firstname,lastName=lastname,gender=gender,profilePicture=profilePicture,address=address,zipCode=zipCode,country=country)

			return render_to_response('index.html', context_instance=RequestContext(request))
	else:
		form = RegistrationForm() # An unbound form
		return render_to_response('register.html', {'form' : form}, context_instance=RequestContext(request))
	return render_to_response('register.html', {'form' : form}, context_instance=RequestContext(request))

def viewUserProfile(request, user_id):
	user = User.objects.get(pk = user_id)
	userEvents = Event.objects.filter(chef=user)
	firstname = user.get_profile().firstName
	lastname = user.get_profile().lastName

	variables = { "firstname" : firstname, "lastname" : lastname, "user" : user, "events" : userEvents}
	return render_to_response('viewUserProfile.html',variables)


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
			mealType = form.cleaned_data['mealType']
			entreeInput = form.cleaned_data['entreeInput']
			firstCourseInput = form.cleaned_data['firstCourseInput']
			secondCourseInput = form.cleaned_data['secondCourseInput']
			dessertInput = form.cleaned_data['dessertInput']
			participantNumber = form.cleaned_data['participantNumber']

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
				event = Event.objects.create(title=title, description=description, chef=theUser, creation_timestamp=datetime.now(), dateOfEvent=date, address=fullAddress, latitude=coordinates[0], longitude=coordinates[1],cuisineType=cuisineType,mealType=mealType,menuEntree=entreeInput,menuFirstCourse=firstCourseInput,menuSecondCourse=secondCourseInput,menuDessert=dessertInput,numberOfParticipants=participantNumber)
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

	flag = False
	e2 = Event.objects.get(pk=event_id)
	allEvents = Event.objects.all()
	guests2 = e2.guests.all()
	numberOfGuests = e2.guests.count()
	reviews = e2.review_set.all()
	firstname = request.user.get_profile().firstName
	lastname = request.user.get_profile().lastName
	notifications = Notify.objects.filter(user=request.user)
	
	#get entree wiki article
	httpRequest = "http://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles=" + e2.menuEntree
	data = urllib2.urlopen(httpRequest)
	djson = data.read()
	myData = json.loads(djson)
	entreeWikiUrl = "http://en.wikipedia.org/wiki?curid=" + str(myData['query']['pages'].items()[0][0])
	
	#get firstCourse wiki article
	httpRequest = "http://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles=" + e2.menuFirstCourse
	data = urllib2.urlopen(httpRequest)
	djson = data.read()
	myData = json.loads(djson)
	firstCourseWikiUrl = "http://en.wikipedia.org/wiki?curid=" + str(myData['query']['pages'].items()[0][0])
	
	#get secondCourse wiki article
	httpRequest = "http://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles=" + e2.menuSecondCourse
	data = urllib2.urlopen(httpRequest)
	djson = data.read()
	myData = json.loads(djson)
	secondCourseWikiUrl = "http://en.wikipedia.org/wiki?curid=" + str(myData['query']['pages'].items()[0][0])
	
	#get dessert wiki article
	httpRequest = "http://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles=" + e2.menuDessert
	data = urllib2.urlopen(httpRequest)
	djson = data.read()
	myData = json.loads(djson)
	dessertWikiUrl = "http://en.wikipedia.org/wiki?curid=" + str(myData['query']['pages'].items()[0][0])
	
	variables = {"event" : e2, "guests" : guests2, "firstname" : firstname, "lastname" : lastname, "userId" : request.user.id, "user" : request.user, "allEvents" : allEvents, "NumberOfGuests" : numberOfGuests, "reviews" : reviews, "notifications" : notifications, "entreeWikiUrl" : entreeWikiUrl, "firstCourseWikiUrl" : firstCourseWikiUrl, "secondCourseWikiUrl" : secondCourseWikiUrl, "dessertWikiUrl" : dessertWikiUrl }
	
	return render_to_response('viewEvent.html', variables)

def reviewEvent(request, event_id):
	e2 = Event.objects.get(pk=event_id)
	print e2.chef
	if request.method == 'POST':
		form = ReviewForm(request.POST)
		if form.is_valid():
			comment = form.cleaned_data['comment']

			#we retrieve the username which will be the chef
			theReviewer = User.objects.get(username=request.user.username)

			#we create an event and save it in the db
			review = Review.objects.create(comment=comment, event=e2, reviewer=theReviewer, review_timestamp=datetime.now())
			review.save()

	guests2 = e2.guests.all()
	reviews = e2.review_set.all()
	numberOfGuests = e2.guests.count()
	variables = {"event" : e2, "guests" : guests2, "NumberOfGuests" : numberOfGuests, "reviews" : reviews}
	return render_to_response('viewEvent.html',variables)


def searchEvents(request):
	notifications = Notify.objects.filter(user=request.user)
	e1 = Event.objects.filter()
	variables = { "outputEvents" : e1, "firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id, "notifications" : notifications}
	return render_to_response('searchEventsResults.html',variables)
	
def viewNotifications(request):

	notifications = Notify.objects.filter(user=request.user)
	
	variables = { "notifications" : notifications, "firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id}
	return render_to_response('viewNotifications.html',variables)

def participateInEvents(request,event_id):
	e3 = Event.objects.get(pk=event_id)
	message = "The user " + str(request.user.username) + " has just requested participation in your event!"
	
	notification = Notify.objects.create(event=e3,sender=request.user,user=e3.chef,text=message, type="ApprovalRequest")
	
	variables = { "firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id, "notification" : notification}
	return render_to_response('joinResult.html',variables)
	
def approveRequest(request, notification_id):
	notification = Notify.objects.get(pk=notification_id)
	e3 = Event.objects.get(pk=notification.event.pk)
	theUser = User.objects.get(username=notification.sender)
	e3.guests.add(theUser)
	e3.save()
	
	message = "The user " + str(request.user.username) + " has approved your request for the event!"
	
	notification = Notify.objects.create(event=e3,sender=request.user,user=notification.sender,text=message, type="ApprovalReply")
	
	Notify.objects.filter(pk=notification_id).delete()
	
	notifications = Notify.objects.filter(user=request.user)
	
	print e3.numberOfParticipants
	print e3.guests.all().count()
	if(e3.guests.all().count() >= e3.numberOfParticipants):
		message = "Your event is now full and closed for participation!"
		notification = Notify.objects.create(event=e3,sender=request.user,user=request.user,text=message, type="FullEvent")
		print notification

	guests = e3.guests.all()
	
	variables = { "firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id, "event" : e3, "guests" : guests, "notifications" : notifications}
	return render_to_response('viewNotifications.html',variables)

def acceptGuestsInEvents(request,event_id):
	event1 = Event.objects.get(pk=event_id)

	#View All the Guests
def deleteEvent(request, event_id):
	#we retrieve the username which will be the chef
	theUser = User.objects.get(username=request.user.username)
	# get all events associated to the user
	e = Event.objects.filter(chef=theUser)
	# create an empty form
	form = createEvent(request)
	
	event = Event.objects.get(pk=event_id)
	
	#notify everyone involved of the deletion of the event
	for guest in event.guests.all():
		message = "The event has been deleted by the owner."	
		notification = Notify.objects.create(event=event,sender=request.user,user=guest,text=message, type="DeleteEvent")
		print notification

	allEvents = Event.objects.all()
	
	Event.objects.filter(pk=event_id).delete()
	# fill out the variables dictionary to pass to the front end
	variables = {"firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id, "events" : e, "form" : form, "allEvents" : allEvents}
	return render_to_response('insert.html', variables)
	
def deleteNotification(request, notification_id):
	Notify.objects.filter(pk=notification_id).delete()

	notifications = Notify.objects.filter(user=request.user)
	
	variables = { "notifications" : notifications, "firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id}
	return render_to_response('viewNotifications.html',variables)

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
					e1 = Event.objects.filter(chef=user).order_by('dateOfEvent')
					e2 = Event.objects.filter(guests=user).order_by('dateOfEvent')
					e3 = e2 | e1
					e = e3.distinct()

					# create an empty form
					form = createEvent(request)

					allEvents = Event.objects.all()
					
					notifications = Notify.objects.filter(user=user)

					# fill out the variables dictionary to pass to the front end
					variables = {"firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id, "events" : e, "form" : form, "allEvents" : allEvents, "notifications" : notifications}
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
