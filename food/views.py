#from django.shortcuts import render
from django.shortcuts import render_to_response
from food.models import Event, Review
from django.contrib.auth.models import User
from django.forms.widgets import Input
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django import forms
from django.template.context import RequestContext
from django.contrib.auth.middleware import AuthenticationMiddleware

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

class Html5EmailInput(Input):
    input_type = 'email'

#this class represents the registration form and its validation methods
class RegistrationForm(forms.Form):
	username = forms.CharField(max_length=30)
	firstname = forms.CharField(max_length=30)
	lastname = forms.CharField(max_length=30)
	email = forms.EmailField(max_length=50, widget=Html5EmailInput())
	password = forms.CharField(max_length=50, widget=forms.PasswordInput())
	passwordConfirmation = forms.CharField(max_length=50, widget=forms.PasswordInput())
	
	# validation method for password field - check if length is 8 chars long at least
	def clean_password(self):
		password = self.cleaned_data['password']
		length = len(password)
		if length < 8:
			raise forms.ValidationError("Password has to be at least 8 characters long.")
		return password
	
	# validation method for username field - check if the user doesnt already exist in db
	def clean_username(self):
		username = self.cleaned_data['username']
		user = User()
		try:
			user = User.objects.get(username=username)
		except user.DoesNotExist:
			return username
		raise forms.ValidationError(u'Username "%s" is already in use.' % username)
		
	# validation method for email - check if the email doesnt already exist in db
	def clean_email(self):
		email = self.cleaned_data['email']
		user = User()
		try:
			user = User.objects.get(email=email)
		except user.DoesNotExist:
			return email
		raise forms.ValidationError(u'Email "%s" is already in use.' % email)
	
	# validation method for password confirmation - check if the password and its confirmation match
	def clean_passwordConfirmation(self):
		passwordConfirmation = self.cleaned_data['passwordConfirmation']
		password = self.cleaned_data['password']
		if password != passwordConfirmation:
			raise forms.ValidationError("Passwords dont match.")
		return password
		
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
			
			return redirect('success') # Redirect after POST
	else:
		form = RegistrationForm() # An unbound form
		return render_to_response('form.html', {'form' : form}, context_instance=RequestContext(request))
	return render_to_response('form.html', {'form' : form}, context_instance=RequestContext(request))

def success(request):
	return HttpResponse('success')