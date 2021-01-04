from django import forms
from .operations import all_names

class RemoveForm(forms.Form):
	name = forms.CharField(max_length=50 , widget = forms.TextInput(attrs={"list" : "namelist"}) )


	def clean_name(self , *args , **kwargs):
		names_all = all_names()
		name = self.cleaned_data.get("name")
		
		if name not in names_all:
			raise forms.ValidationError("Name is not in the record")

		return name


class LoanForm(forms.Form):
	name = forms.CharField(max_length=50 , widget = forms.TextInput(attrs={"list" : "namelist"}))
	amount = forms.IntegerField()
	installment = forms.IntegerField()

	def clean_name(self , *args , **kwargs):
		names_all = all_names()
		name = self.cleaned_data.get("name")
		
		if name not in names_all:
			raise forms.ValidationError("Name is not in the record")

		return name


class PaidForm(forms.Form):
	name = forms.CharField(max_length=50 , widget = forms.TextInput(attrs={"list" : "namelist"}))
	installment = forms.IntegerField()

	def clean_name(self , *args , **kwargs):
		names_all = all_names()
		name = self.cleaned_data.get("name")
		
		if name not in names_all:
			raise forms.ValidationError("Name is not in the record")

		return name


class JoinForm(forms.Form):
	Username = forms.CharField(max_length = 50 , widget=forms.TextInput(attrs={'placeholder': 'Without Space'}))
	FirstName = forms.CharField(max_length=50)
	LastName = forms.CharField(max_length=50)
	password = forms.CharField(max_length=50 , widget=forms.PasswordInput)
	cd = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Enter CD'}))

	def clean(self , *args , **kwargs):
		names_all = all_names()
		first = self.cleaned_data.get("FirstName")
		last = self.cleaned_data.get("LastName")
		
		if f"{first.upper()} {last.upper()}" in names_all:
			raise forms.ValidationError("This user is already in the record")

