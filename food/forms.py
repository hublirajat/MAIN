from django import forms
from django.forms.widgets import Input

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