from django import forms
from adminapp.operations import all_users
# from django import widget


class Memberform(forms.Form):
	username = forms.CharField(max_length=100 , widget = forms.TextInput(attrs={'placeholder': 'Enter Username'}))
	password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Enter Password'}))


class ChangePassword(forms.Form):
	password = forms.CharField(max_length=50 ,widget = forms.PasswordInput(attrs={'placeholder': 'New Password'}))
	password2 = forms.CharField(max_length=50 , widget = forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))


	def clean(self , *args , **kwargs):

		if self.cleaned_data.get("password") != self.cleaned_data.get("password2"):
			raise forms.ValidationError("Both fields should match!!")



