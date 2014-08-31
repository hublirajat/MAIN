from django.shortcuts import render_to_response
from food.models import Event, Review, UserProfile, Notify, Message, UserReviews
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
from food.forms import EventCreationForm, ReviewForm, RegistrationForm, UserReviewForm
from datetime import datetime
import os
os.environ['http_proxy']=''
import urllib
import urllib2
import settings
import json
from django.db.models import Q
from django.core import serializers
from django.contrib.auth.models import AnonymousUser
import re
import unicodedata
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

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
	
	return render_to_response("indexGuil.html", variables, context_instance=RequestContext(request))

############################################################################################################################################

# this class represents the email input form field for validation
class Html5EmailInput(Input):
    input_type = 'email'

# Following views are all User Related Views
# method to register a new user - first checks if the form is valid and then registers a new user
def registerNewUser(request):
	if request.method == 'POST': # If the form has been submitted...
		form = RegistrationForm(request.POST,request.FILES) # A form bound to the POST data

		if form.is_valid(): # All validation rules pass
			username = form.cleaned_data['username']
			firstname = form.cleaned_data['firstname']
			lastname = form.cleaned_data['lastname']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			passwordConfirmation = form.cleaned_data['passwordConfirmation']
			gender = form.cleaned_data['gender']
			#profilePicture = form.cleaned_data['profilePicture']
			address = form.cleaned_data['address']
			zipCode = form.cleaned_data['zipCode']
			country = form.cleaned_data['country']

			try:
				#thePic = request.FILES['profilePicture']
				#thePath = settings.MEDIA_ROOT+'/uploadedPics/'+str(profilePicture)
				#path = default_storage.save(thePath, ContentFile(thePic.read()))		
					
				# we now register the user
				user = User.objects.create_user(username=username,email=email,password=password)
				profile = UserProfile.objects.create(user=user,firstName=firstname,lastName=lastname,gender=gender,address=address,zipCode=zipCode,country=country)
				
			except Exception as e:
				print '%s (%s)' % (e.message, type(e))

			return render_to_response('index.html', context_instance=RequestContext(request))
	else:
		form = RegistrationForm() # An unbound form
		return render_to_response('register.html', {'form' : form}, context_instance=RequestContext(request))
	return render_to_response('register.html', {'form' : form}, context_instance=RequestContext(request))

def viewUserProfile(request, event_id):

	# Getting the Chef of the Event
	event1 = Event.objects.get(pk=event_id)
	eventChef = event1.chef

	# Getting the user from User who is the Event Chef
	# User does not contain the same attributes as UserProfile
	user1 = User.objects.get(username = eventChef)

	# Getting All Events for the User
	# Result stored in an Event object namely myEvents
	myEvents = user1.event_chef.all()

	# Getting User Details from User Profile for the User
	# userprofile contains all details such as:
	# - userReview
	# - ratingStars
	userprofile = UserProfile.objects.get(user = user1)

	userreviews = []

	if UserReviews.objects.filter(user = user1):
		userreviews = UserReviews.objects.filter(user = user1)

	#very ugly solution, needs to be re-thinked
	'''profilePicture = user.get_profile().profilePicture.path
	splitProf = profilePicture.split('/')
	splitProf.pop(0)
	splitProf.pop(0)
	splitProf.pop(0)
	splitProf.pop(0)
	myString = "/".join(splitProf)
	myString = '/'+myString'''

	# Sending 2 objects to the html page, namely:
	# - userprofile: UserProfile
	# - events: Event
	# - user: User
	
	globalRating = calculateGlobalRating(userreviews,0)

	# profilePicture should be sent inside userprofile, but logic needs to be done on the frontend
	variables = { "userprofile" : userprofile, "userreviews" : userreviews, "events" : myEvents, "user" : request.user, "globalrating" : globalRating}
	return render_to_response('profil.html',variables)

def reviewUser(request, user_id):
	#e2 = Event.objects.get(pk=event_id)
	print user_id
	userprofile = UserProfile.objects.get(id = user_id)
	user1 = User.objects.get(username = userprofile.user)
	if request.method == 'POST':
		print "Check"
		form = UserReviewForm(request.POST)
		if form.is_valid():
			print "Check"
			rating = form.cleaned_data['rating']
			textReview = form.cleaned_data['userReview']

			# Get the user reviews from UserReviews userprofile
			# ToDo: Calculate accurately User Review

			#Get the Reviewer who reviews User Profile
			theReviewer = User.objects.get(username=request.user.username)

			UserReviews.objects.create(reviewer=theReviewer, user=user1, userReview=textReview, ratingStars=rating)
			
			userreviews = UserReviews.objects.get(user = user1)
			
			globalRating = calculateGlobalRating(userreviews,rating)
				

	user1 = User.objects.get(username = userprofile.user)
	myEvents = user1.event_chef.all()

	variables = { "userreviews" : userreviews, "events" : myEvents, "userprofile" : userprofile, "globalrating" : globalrating}
	return render_to_response('viewUserProfile.html',variables)

# Following views are all Event Related Views
# method to create a new event on the dashboard
def createEvent(request):
	if request.method == 'POST':
		form = EventCreationForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			description = form.cleaned_data['description']
			date = form.cleaned_data['date']

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
	entreeWikiUrl = ""
	firstCourseWikiUrl = ""
	secondCourseWikiUrl = ""
	dessertWikiUrl = ""
	
	#get entree wiki article
	if(e2.menuEntree):
		entree = normalizeWikiLink(e2.menuEntree)
		httpRequest = "http://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles=" + entree
		data = urllib2.urlopen(httpRequest)
		djson = data.read()
		myData = json.loads(djson)
		entreeWikiUrl = "http://en.wikipedia.org/wiki?curid=" + str(myData['query']['pages'].items()[0][0])
	
	if(e2.menuFirstCourse):
		#get firstCourse wiki article
		firstCourse = normalizeWikiLink(e2.menuFirstCourse)
		httpRequest = "http://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles=" + firstCourse
		data = urllib2.urlopen(httpRequest)
		djson = data.read()
		myData = json.loads(djson)
		firstCourseWikiUrl = "http://en.wikipedia.org/wiki?curid=" + str(myData['query']['pages'].items()[0][0])
	
	if(e2.menuSecondCourse):
		#get secondCourse wiki article
		secondCourse = normalizeWikiLink(e2.menuSecondCourse)
		httpRequest = "http://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles=" + secondCourse

		data = urllib2.urlopen(httpRequest)
		djson = data.read()
		myData = json.loads(djson)
		secondCourseWikiUrl = "http://en.wikipedia.org/wiki?curid=" + str(myData['query']['pages'].items()[0][0])
	
	if(e2.menuDessert):
		#get dessert wiki article
		dessert = normalizeWikiLink(e2.menuDessert)
		httpRequest = "http://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles=" + dessert
		data = urllib2.urlopen(httpRequest)
		djson = data.read()
		myData = json.loads(djson)
		dessertWikiUrl = "http://en.wikipedia.org/wiki?curid=" + str(myData['query']['pages'].items()[0][0])
	
	variables = {"event" : e2, "guests" : guests2, "firstname" : firstname, "lastname" : lastname, "userId" : request.user.id, "user" : request.user, "allEvents" : allEvents, "NumberOfGuests" : numberOfGuests, "reviews" : reviews, "notifications" : notifications, "entreeWikiUrl" : entreeWikiUrl, "firstCourseWikiUrl" : firstCourseWikiUrl, "secondCourseWikiUrl" : secondCourseWikiUrl, "dessertWikiUrl" : dessertWikiUrl }
	
	return render_to_response('viewEvent.html', variables)

# this method represents the act of reviewing a given event
def reviewEvent(request, event_id):

	# - Get the corresponding event from Events for event_id
	# - Creation of ReviewForm in forms.py
	# - Defining comment as an attribute of ReviewForm
	# - Get Reviewer and then create review in Review for the reviewer
	e2 = Event.objects.get(pk=event_id)

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
	return render_to_response('viewEvent.html',variables, context_instance=RequestContext(request))


def searchEvents(request):
	notifications = Notify.objects.filter(user=request.user)
	e1 = Event.objects.filter()
	variables = { "outputEvents" : e1, "firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id, "notifications" : notifications}
	return render_to_response('searchEventsResults.html',variables, context_instance=RequestContext(request))

# this method is showing all the users notifications	
def viewNotifications(request):

	notifications = Notify.objects.filter(user=request.user)
	
	variables = { "notifications" : notifications, "firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id}
	return render_to_response('viewNotifications.html',variables, context_instance=RequestContext(request))

# this method is showing all the users messages	
def viewMessages(request):

	messages = Message.objects.filter(user=request.user)
	
	variables = { "messages" : messages, "firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id}
	return render_to_response('viewMessages.html',variables, context_instance=RequestContext(request))

# this method is treating the functionality of a user requesting participation in a given event
def participateInEvents(request,event_id):
	e3 = Event.objects.get(pk=event_id)
	message = "The user " + str(request.user.username) + " has just requested participation in your event!"
	
	notification = Notify.objects.create(event=e3,sender=request.user,user=e3.chef,text=message, type="ApprovalRequest")
	
	variables = { "firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id, "notification" : notification}
	return render_to_response('joinResult.html',variables, context_instance=RequestContext(request))

# this method represents the functionality of accepting a request for participation in a given event	
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
	

	if(e3.guests.all().count() >= e3.numberOfParticipants):
		message = "Your event is now full and closed for participation!"
		notification = Notify.objects.create(event=e3,sender=request.user,user=request.user,text=message, type="FullEvent")

	guests = e3.guests.all()
	
	variables = { "firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id, "event" : e3, "guests" : guests, "notifications" : notifications}
	return render_to_response('viewNotifications.html',variables, context_instance=RequestContext(request))

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

	allEvents = Event.objects.all()
	
	Event.objects.filter(pk=event_id).delete()
	# fill out the variables dictionary to pass to the front end
	variables = {"firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id, "events" : e, "form" : form, "allEvents" : allEvents}
	return render_to_response('insert.html', variables, context_instance=RequestContext(request))

# this method deletes a given notification	
def deleteNotification(request, notification_id):
	Notify.objects.filter(pk=notification_id).delete()

	notifications = Notify.objects.filter(user=request.user)
	
	variables = { "notifications" : notifications, "firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id}
	return render_to_response('viewNotifications.html',variables, context_instance=RequestContext(request))

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

					userCoordinates = get_coordinates(request, user.get_profile().address, user.get_profile().zipCode, user.get_profile().country)
					
					#allEvents = Event.objects.all()
					allEvents = returnEventsInRange(userCoordinates[0],userCoordinates[1],10,request)
					
					notifications = Notify.objects.filter(user=user)

					# fill out the variables dictionary to pass to the front end
					variables = {"firstname" : request.user.get_profile().firstName, "lastname" : request.user.get_profile().lastName, "userId" : request.user.id, "events" : e, "form" : form, "allEvents" : allEvents, "notifications" : notifications}
					return render_to_response('indexGuil.html', variables)
			else:
				messages.error(request, 'Wrong password for user ' + username)
	return render_to_response('index.html', context_instance=RequestContext(request))

# this method gives back coordinates [latitude,longitude] for a given address
# it is using google maps geocoding API for the request
def get_coordinates(request,address,zipCode,country):

	print address
	print zipCode
	print country

	coordinates = (0,0)
	address = urllib.quote_plus(address)
	httpRequest = "http://maps.google.com/maps/api/geocode/json?address=" + address + "," + zipCode + "," + country
	
	print httpRequest
	
	data = urllib2.urlopen(httpRequest)
	djson = data.read()
	myData = json.loads(djson)
	if(myData['status'] == 'OK'):
		latitude = myData['results'][0]['geometry']['location']['lat']
		longitude = myData['results'][0]['geometry']['location']['lng']
		coordinates = (latitude,longitude)
		return coordinates
	else:
		return coordinates

# this method takes a latitude, longitude and zoom factor, and returns the events in a given range
# returning them in JSON format if the call is AJAX and as a queryset otherwise
def returnEventsInRange(latitude,longitude,zoomFactor,request):
	#this dictionary has the correspondance between the zoom factor and the coordinate degrees
	zoomFactorDictionary = {'0': 360, '1': 180, '2': 90, '3': 45, '4': 22.5, '5': 11.25, '6': 5.625, '7': 2.813, '8': 1.406, '9': 0.703, '10': 0.352, '11': 0.176, '12': 0.088, '13': 0.044, '14': 0.022, '15': 0.011, '16': 0.005, '17': 0.003, '18': 0.001, '19': 0.0005}
	
	degreeFactor = zoomFactorDictionary[str(zoomFactor)]
		
	latitude = float(latitude)
	longitude = float(longitude)
	
	eventsInRangeList = {}
	
	try:
		latitudeLTE = latitude+degreeFactor
		latitudeGTE = latitude-degreeFactor
		longitudeLTE = longitude+degreeFactor
		longitudeGTE = longitude-degreeFactor
		eventsInRange = Event.objects.filter(latitude__lte=(latitudeLTE)).filter(latitude__gte=(latitudeGTE)).filter(longitude__lte=(longitudeLTE)).filter(longitude__gte=(longitudeGTE))
		eventsInRangeJSON = serializers.serialize('json', eventsInRange, fields=('pk','title','description','address','chef','latitude','longitude','cuisineType'))
	except Exception as e:
		print '%s (%s)' % (e.message, type(e))
	
	if(request.is_ajax()):
		return eventsInRangeJSON
	else:
		return eventsInRange

# this method is managing the asynchronous calls to the map and retrieving only the events in focus (in a given range, depending on the zoom factor)
def ajaxMapRefresh(request):
	if request.is_ajax():
		zoomFactor = request.POST['zoomFactor']
		userLatitude = request.POST['userLatitude']
		userLongitude = request.POST['userLongitude']
		userId = request.POST['userId']
		allEvents = returnEventsInRange(userLatitude,userLongitude,zoomFactor,request)                                                                 
		return HttpResponse(json.dumps(allEvents,ensure_ascii=False), mimetype='application/javascript')
		
def normalizeWikiLink(string):

	string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')
	# Remove all non-word characters (everything except numbers and letters)
	string = re.sub(r"[^\w\s]", '', string)
	# Replace all runs of whitespace with a single dash
	string = re.sub(r"\s+", '_', string)
	return string
	
def calculateGlobalRating(userreviews,rating):
	globalRating = 0
			
	for review in userreviews:
		oldrating = review.ratingStars
		if rating==0:
			globalRating = oldrating
		else :
			globalRating = (oldrating + rating)/2
	
	return globalRating
	
def loadUserProfilePersonalPageAJAX(request):
	userList = []
	try:
		if request.is_ajax():
			print 'this is the user doing the ajax request' + request.user.username
			theUser = User.objects.get(username=request.user.username)
			userList.append(theUser)
			print userList
			jsonString = serializers.serialize('json', userList, fields=('username','name','surname','gender','address'))
			print 'json is : ' +jsonString
			return HttpResponse(json.dumps(jsonString,ensure_ascii=False), mimetype='application/javascript')
	except Exception as e:
		print '%s (%s)' % (e.message, type(e))
		