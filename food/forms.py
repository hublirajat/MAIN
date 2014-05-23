from django import forms
from django.forms.widgets import Input
from django.contrib.auth.models import User
import datetime

#defines country list for address drop down list
countryList = ([('Afghanistan','Afghanistan'), ('Albania','Albania'), ('Algeria','Algeria'), ('Andorra','Andorra'), ('Angola','Angola'), ('Antigua and Barbuda','Antigua and Barbuda'), ('Argentina','Argentina'), ('Armenia','Armenia'), ('Aruba','Aruba'), ('Australia','Australia'), ('Austria','Austria'), ('Azerbaijan','Azerbaijan'), ('Bahamas','Bahamas'), ('Bahrain','Bahrain'), ('Bangladesh','Bangladesh'), ('Barbados','Barbados'), ('Belarus','Belarus'), ('Belgium','Belgium'), ('Belize','Belize'), ('Benin','Benin'), ('Bhutan','Bhutan'), ('Bolivia','Bolivia'), ('Bosnia and Herzegovina','Bosnia and Herzegovina'), ('Botswana','Botswana'), ('Brazil','Brazil'), ('Brunei','Brunei'), ('Bulgaria','Bulgaria'), ('Burkina Faso','Burkina Faso'), ('Burma','Burma'), ('Burundi','Burundi'), ('Cambodia','Cambodia'), ('Cameroon','Cameroon'), ('Canada','Canada'), ('Cape Verde','Cape Verde'), ('Central African Republic','Central African Republic'), ('Chad','Chad'), ('Chile','Chile'), ('China','China'), ('Colombia','Colombia'), ('Comoros','Comoros'), ('Congo, Democratic Republic','Congo, Democratic Republic'), ('Congo, Republic','Congo, Republic'), ('Costa Rica','Costa Rica'), ("Cote d'Ivoire","Cote d'Ivoire"), ('Croatia','Croatia'), ('Cuba','Cuba'), ('Curacao','Curacao'), ('Cyprus','Cyprus'), ('Czech Republic','Czech Republic'), ('Denmark','Denmark'), ('Djibouti','Djibouti'), ('Dominica','Dominica'), ('Dominican Republic','Dominican Republic'), ('East Timor','East Timor'), ('Ecuador','Ecuador'), ('Egypt','Egypt'), ('El Salvador','El Salvador'), ('Equatorial Guinea','Equatorial Guinea'), ('Eritrea','Eritrea'), ('Estonia','Estonia'), ('Ethiopia','Ethiopia'), ('Fiji','Fiji'), ('Finland','Finland'), ('France','France'), ('Gabon','Gabon'), ('Gambia','Gambia'), ('Georgia','Georgia'), ('Germany','Germany'), ('Ghana','Ghana'), ('Greece','Greece'), ('Grenada','Grenada'), ('Guatemala','Guatemala'), ('Guinea','Guinea'), ('Guinea-Bissau','Guinea-Bissau'), ('Guyana','Guyana'), ('Haiti','Haiti'), ('Holy See','Holy See'), ('Honduras','Honduras'), ('Hong Kong','Hong Kong'), ('Hungary','Hungary'), ('Iceland','Iceland'), ('India','India'), ('Indonesia','Indonesia'), ('Iran','Iran'), ('Iraq','Iraq'), ('Ireland','Ireland'), ('Israel','Israel'), ('Italy','Italy'), ('Jamaica','Jamaica'), ('Japan','Japan'), ('Jordan','Jordan'), ('Kazakhstan','Kazakhstan'), ('Kenya','Kenya'), ('Kiribati','Kiribati'), ('Korea, North','Korea, North'), ('Korea, South','Korea, South'), ('Kosovo','Kosovo'), ('Kuwait','Kuwait'), ('Kyrgyzstan','Kyrgyzstan'), ('Laos','Laos'), ('Latvia','Latvia'), ('Lebanon','Lebanon'), ('Lesotho','Lesotho'), ('Liberia','Liberia'), ('Libya','Libya'), ('Liechtenstein','Liechtenstein'), ('Lithuania','Lithuania'), ('Luxembourg','Luxembourg'), ('Macau','Macau'), ('Macedonia','Macedonia'), ('Madagascar','Madagascar'), ('Malawi','Malawi'), ('Malaysia','Malaysia'), ('Maldives','Maldives'), ('Mali','Mali'), ('Malta','Malta'), ('Marshall Islands','Marshall Islands'), ('Mauritania','Mauritania'), ('Mauritius','Mauritius'), ('Mexico','Mexico'), ('Micronesia','Micronesia'), ('Moldova','Moldova'), ('Monaco','Monaco'), ('Mongolia','Mongolia'), ('Montenegro','Montenegro'), ('Morocco','Morocco'), ('Mozambique','Mozambique'), ('Namibia','Namibia'), ('Nauru','Nauru'), ('Nepal','Nepal'), ('Netherlands','Netherlands'), ('Netherlands Antilles','Netherlands Antilles'), ('New Zealand','New Zealand'), ('Nicaragua','Nicaragua'), ('Niger','Niger'), ('Nigeria','Nigeria'), ('North Korea','North Korea'), ('Norway','Norway'), ('Oman','Oman'), ('Pakistan','Pakistan'), ('Palau','Palau'), ('Palestinian Territories','Palestinian Territories'), ('Panama','Panama'), ('Papua New Guinea','Papua New Guinea'), ('Paraguay','Paraguay'), ('Peru','Peru'), ('Philippines','Philippines'), ('Poland','Poland'), ('Portugal','Portugal'), ('Qatar','Qatar'), ('Romania','Romania'), ('Russia','Russia'), ('Rwanda','Rwanda'), ('Saint Kitts and Nevis','Saint Kitts and Nevis'), ('Saint Lucia','Saint Lucia'), ('Saint Vincent and the Grenadines','Saint Vincent and the Grenadines'), ('Samoa ','Samoa '), ('San Marino','San Marino'), ('Sao Tome and Principe','Sao Tome and Principe'), ('Saudi Arabia','Saudi Arabia'), ('Senegal','Senegal'), ('Serbia','Serbia'), ('Seychelles','Seychelles'), ('Sierra Leone','Sierra Leone'), ('Singapore','Singapore'), ('Sint Maarten','Sint Maarten'), ('Slovakia','Slovakia'), ('Slovenia','Slovenia'), ('Solomon Islands','Solomon Islands'), ('Somalia','Somalia'), ('South Africa','South Africa'), ('South Sudan','South Sudan'), ('Spain','Spain'), ('Sri Lanka','Sri Lanka'), ('Sudan','Sudan'), ('Suriname','Suriname'), ('Swaziland','Swaziland'), ('Sweden','Rwanda'), ('Switzerland','Switzerland'), ('Syria','Syria'), ('Taiwan','Taiwan'), ('Tajikistan','Tajikistan'), ('Tanzania','Tanzania'), ('Thailand','Thailand'), ('Togo','Togo'), ('Tonga','Tonga'), ('Trinidad and Tobago','Trinidad and Tobago'), ('Tunisia','Tunisia'), ('Turkey','Turkey'), ('Turkmenistan','Turkmenistan'), ('Tuvalu','Tuvalu'), ('Uganda','Uganda'), ('Ukraine','Ukraine'), ('United Arab Emirates','United Arab Emirates'), ('United Kingdom','United Kingdom'), ('Uruguay','Uruguay'), ('Uzbekistan','Uzbekistan'), ('Vanuatu','Vanuatu'), ('Venezuela','Venezuela'), ('Vietnam','Vietnam'), ('Yemen','Yemen'), ('Zambia','Zambia'), ('Zimbabwe','Zimbabwe'),])

cuisineTypeList = ([('African','African'), ('Anglo-Saxon','Anglo-Saxon'), ('Arab','Arab'), ('Asian','Asian'), ('Barbecue','Barbecue'), ('Continental','Continental'), ('Experimental','Experimental'), ('Fusion','Fusion'), ('Indian','Indian'), ('Italian','Italian'), ('Kosher','Kosher'), ('Mediterranean','Mediterranean'), ('Mexican','Mexican'), ('Middle-East','Middle-East'),  ('Nordic','Nordic'),  ('Nouvelle','Nouvelle'),  ('Oceanian','Oceanian'),  ('Sushi','Sushi'),  ('Vegan','Vegan'), ('Vegetarian','Vegetarian'),])

mealTypeList = ([('Breakfast','Breakfast'), ('Lunch','Lunch'), ('Dinner','Dinner'), ('Brunch','Brunch'), ('Snack','Snack'),])

class Html5EmailInput(Input):
    input_type = 'email'

# this class represents the event creation form and its validation methods
class EventCreationForm(forms.Form): 
	title = forms.CharField(max_length=100, required=True)
	description = forms.CharField(max_length=300, required=True)
	# this field is using a widget -> jquery datepicker (defined as a javascript in the template header)
	date = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))
	cuisineType = forms.ChoiceField(choices=cuisineTypeList, initial='African', required = True,)
	mealType = forms.ChoiceField(choices=mealTypeList, initial='Breakfast', required = True,)
	address = forms.CharField(max_length=200)
	zipCode = forms.CharField(max_length=5)
	country = forms.ChoiceField(choices=countryList, initial='France', required = True,)
	entreeInput = forms.CharField(max_length=100)
	firstCourseInput = forms.CharField(max_length=100)
	secondCourseInput = forms.CharField(max_length=100)
	dessertInput = forms.CharField(max_length=100)
	participantNumber = forms.ChoiceField(choices=((str(x), x) for x in range(1,100)))
	
	def clean_zipCode(self):
		zipCode = self.cleaned_data['zipCode']
		if not (zipCode.isdigit()):
			raise forms.ValidationError("Zip / Postal code must be a number!")
		return zipCode
		
	def clean_date(self):
		date = self.cleaned_data['date']
		if (date < datetime.date.today()):
			raise forms.ValidationError("Event must be created in the future, not the past!")
		return date

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