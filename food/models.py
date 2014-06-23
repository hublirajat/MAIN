from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# this class models an Event
class Event(models.Model):
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=200)
	chef = models.ForeignKey(User, related_name='event_chef')
	guests = models.ManyToManyField(User, related_name='event_guests')
    #reviews = models.ForeignKey('Review')
	creation_timestamp = models.DateTimeField(auto_now_add=True)
	dateOfEvent = models.DateTimeField()
	address = models.CharField(max_length=200)
	latitude = models.FloatField(max_length=100)
	longitude = models.FloatField(max_length=100)
	cuisineType = models.CharField(max_length=100)
	mealType = models.CharField(max_length=100)
	menuEntree = models.CharField(max_length=100)
	menuFirstCourse = models.CharField(max_length=100)
	menuSecondCourse = models.CharField(max_length=100)
	menuDessert = models.CharField(max_length=100)
	numberOfParticipants = models.IntegerField(max_length=100)

	def __unicode__(self):
		return self.description

# this class models a review 
class Review(models.Model):
    comment = models.CharField(max_length=500)
    event = models.ForeignKey(Event)
    reviewer = models.ForeignKey(User)
    review_timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.comment
    def reviewer_comments_event(self, text):
        comment = text
        sender = review.reviewer
        event = review.event

        notify = Notify()
        notify.event = event
        notify.sender = sender
        notify.user = event.chef
        notify.text = text
        notify.save()

# this class models a like
class Likes(models.Model):
    event = models.ForeignKey(Event)
    liker = models.ForeignKey(User, related_name='event_liker')

    def __unicode__(self):
        return '%s' % (self.liker)

# this class models a notification
class Notify(models.Model):
	event = models.ForeignKey(Event)
	notificationSender = models.ForeignKey(User, related_name="notificationSender")
	user = models.ForeignKey(User, related_name="notificationUser")
	text = models.CharField(max_length=200)
	type = models.CharField(max_length=100)

	def __unicode__(self):
		return self.text + self.type + str(self.user) + str(self.sender)
		
# this class models a message
class Message(models.Model):
	messageSender = models.ForeignKey(User, related_name="messageSender")
	user = models.ForeignKey(User, related_name="messageUser")
	text = models.CharField(max_length=200)

	def __unicode__(self):
		return self.text + self.type + str(self.user) + str(self.sender)

# this class models the user profile - it extends the regular User class, in order to add more fields
class UserProfile(models.Model):  
	user = models.ForeignKey(User, unique=True)
	firstName = models.CharField(max_length=30)
	lastName = models.CharField(max_length=30)
	address = models.CharField(max_length=140)  
	gender = models.CharField(max_length=140)  
	profilePicture = models.ImageField(upload_to='/staticfiles/uploadedPics/', default="/staticfiles/img/default_profile.jpg")
	address = models.CharField(max_length=200)
	zipCode = models.CharField(max_length=5)
	country = models.CharField(max_length=100)

	def __unicode__(self):
		return u'Profile of user: %s' % self.user.username
