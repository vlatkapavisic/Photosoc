from django import forms
import re
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

class RegistrationForm(forms.Form):
	username = forms.CharField(label=u'Username', max_length=30)
	first_name = forms.CharField(label=u'First name', max_length=30)
	last_name = forms.CharField(label=u'Last name', max_length=30)
	email = forms.EmailField(label=u'Email')
	password1 = forms.CharField(
		label=u'Password',
		widget=forms.PasswordInput()
	)
	password2 = forms.CharField(
		label=u'Password (Again)',
		widget=forms.PasswordInput()
	)
	
	def clean_password2(self):
		if 'password1' in self.cleaned_data:
			password1 = self.cleaned_data['password1']
			password2 = self.cleaned_data['password2']
			if password1 == password2:
				return password2
		raise forms.ValidationError('Passwords do not match.')
		
	def clean_username(self):
		username = self.cleaned_data['username']
		if not re.search(r'^\w+$', username):
			raise forms.ValidationError('Username can only contain '
			'alphanumeric characters and the underscore.')
		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('Username is already taken.')
		
		
class PhotoUploadForm(forms.Form):
	photo=forms.ImageField(label=u'Select a photo')
	caption=forms.CharField(
		label=u'Caption',
		widget=forms.TextInput(attrs={'size': 64})
		)
	private=forms.BooleanField(
		label=u'Private',
		required=False,
		widget=forms.CheckboxInput()
		)
	tags=forms.CharField(
		label=u'Tags',
		required=False,
		widget=forms.TextInput(attrs={'size': 64})
		)
		
class PhotoTagForm(forms.Form):
	tags=forms.CharField(
		label=u'Tags',
		help_text=u'Enter the users names separated by double spaces',
		widget=forms.TextInput(attrs={'size': 64})
		)
