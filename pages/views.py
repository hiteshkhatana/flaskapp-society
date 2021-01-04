from django.http import HttpResponseRedirect
from django.shortcuts import render , redirect , get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

from django.contrib import messages
from adminapp.operations import *
from adminapp.operations import all_names


from django.conf import settings 
from django.core.mail import EmailMessage

from .forms import Memberform, ChangePassword

import random


# Create your views here.
def home_view(request):

	add_next_month()
	
	my_form = Memberform()
	context = {
	"member_form" : my_form
	}


	if request.method == 'POST':
		if request.user.is_authenticated:
			if request.user.is_superuser:
				return redirect('/adminmainpage')
			else:
				name = request.user.get_full_name()
				return redirect(f"/membersrecord/{name}")

		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			if user.is_superuser:
				return redirect('/adminmainpage')
			else:
				name = request.user.get_full_name()
				return redirect(f"/membersrecord/{name}")

		
		else:
			messages.info(request, 'Username OR password is incorrect')



	else:
		if request.user.is_authenticated:
			if request.user.is_superuser:
				return redirect('/adminmainpage')
			else:
				name = request.user.get_full_name()
				return redirect(f"/membersrecord/{name}")

	return render( request, "home.html" ,context)


def log_out(request):
	logout(request)
	return redirect('/')
	
@login_required(login_url="/")
def print_view(request):

	objlist = onemonth_record(request.session["month_selected"])

	context = {
	"data"  :objlist
	}

	return render(request , "print_template.html" , context)



@login_required(login_url="/")
def password_reset_view(request):

	name = request.user.get_full_name()
	email_addrs = request.user.email
	if email_addrs == "":

		context = {
		"infoline" : f"Hi {name} , Your email is not registered , please contact admin",
		"status"  : "noaction"
		}

	else:
		context = {
		"infoline" : f"Hi {name} , Otp will be sent to your registered email address : {email_addrs}",
		'status' : 'entry'
		}

	if request.method == 'POST':
		
		print(request)
		print(email_addrs)
		print(name)


		otp = send_email(email_addrs ,name )

		request.session["otp"] = otp

		return redirect("/otpvalidation")

	return render(request , "password_reset.html" , context)


def send_email(email_id , name ):
	otp = random.randint(1111,9999)

	template = render_to_string("message_template.html" , {'name' : name , 'otp' : otp})

	email = EmailMessage(subject='Reset password' , body=template , from_email=settings.EMAIL_HOST_USER , to=[email_id])

	email.fail_silently = False
	email.send()

	return otp


@login_required(login_url="/")
def validate_otp(request):

	context = {
		'status' : 'otp-validation'
	}

	if request.method == "POST":
		val = request.POST.get("otp")

		if int(val) == int(request.session["otp"]):
			return redirect("/changepassword")
		else:
			messages.info(request , "sorry , OTP does not match !!! ( Please try again )")


	return render(request , "password_reset.html" , context)


@login_required(login_url="/")
def new_password(request):

	change_form = ChangePassword()
	User = request.user

	context = {
	"form2" : change_form,
	"status" : "new-password"
	}

	if request.method == "POST":
		change_form = ChangePassword(request.POST)
		context = {
		"form2" : change_form,
		"status" : "new-password"
		}

		if change_form.is_valid():
			new_pass = request.POST.get("password")
			User.set_password(new_pass)
			User.save()
			messages.info(request ,"Password is changed successfully!!!")
			return redirect("/")

	return render(request,"password_reset.html" , context)