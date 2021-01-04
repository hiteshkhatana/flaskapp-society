from django.shortcuts import render , get_list_or_404 ,redirect , reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User


from members.models import Members
from .operations import *
from .forms import RemoveForm , LoanForm , PaidForm , JoinForm

# Create your views here.




@login_required(login_url="/")
def adminmainpage_view(request):
	
	add_next_month()

	options = all_months()
	context = {
	"options" : options,
	"data"  : None,
	"selected" : "Select",
	"cd" : None,
	"install" : None,
	"interest" : None,
	"total"  : None,
	"bal" : None,
	"tot_interest"  : None,
	}

	if request.method == "POST":
		selected = request.POST["month_options"]

		request.session["month_selected"] = selected

		if selected != "Select":

			objlist = onemonth_record(selected)

			cd , install , interest, total , bal , tot_interest = month_updates(selected)

			context = {
			"options" : options,
			"data"  :objlist,
			"month" : f" Record of {selected}",
			"selected" : selected,
			"cd" : f"CD : {cd}",
			"install" : f"INSTALLMENT : {install}",
			"interest" : f"INTEREST : {interest}",
			"total"  :f"TOTAL : {total}",
			"bal" : f"LOAN BAL : {bal}",
			"tot_interest"  : f"Total INTEREST Collected : {tot_interest}",
			}

	return render(request , "adminapp/adminmain.html" , context)

@login_required(login_url="/")
def remove_form_view(request):
	names_all = all_names()
	names_all = set(names_all)

	formobj = RemoveForm()
	context = {
	"form" : formobj,
	"confirm" : "no",
	"names" : names_all
	}

	if request.method == "POST":

		formobj = RemoveForm(request.POST)
		context = {
		"form" : formobj,
		"confirm" : "no",
		"names" : names_all
		}

		if formobj.is_valid():
			
			name = request.POST.get("name")

			return redirect(f"/confirmform/{name}")
					

	return render(request , "adminapp/removeform.html" , context)

@login_required(login_url="/")
def confirmform_view(request , name):

	cd_total = total_cd(name)

	context = {
	"confirm" : "yes",
	"name" : name,
	"cd" : cd_total
	}

	if request.method == "POST":
		if request.POST.get('submit2') == "Yes":
			remove_entry(name)
			messages.info(request , f"{name} is removed successfully !!!!!")
			return redirect('/remove')

		elif request.POST.get('submit2') == "No":
			return redirect('/remove')

	return render(request , "adminapp/removeform.html" , context)

@login_required(login_url="/")
def loan_form_view(request):
	names_all = all_names()
	names_all = set(names_all)

	formobj = LoanForm()
	context = {
	"form" : formobj,
	"names" : names_all
	}

	if request.method == "POST":

		formobj = LoanForm(request.POST)
		context = {
		"form" : formobj,
		"names" : names_all
		}

		if formobj.is_valid():
			
			name = request.POST.get("name")
			amount = request.POST.get("amount")
			installment = request.POST.get("installment")

			loan_entry(name ,int(amount) ,int(installment))

			messages.info(request , "updated successfully !!!!!!!!!!!!!")
					
	formobj = LoanForm()
	context = {
	"form" : formobj,
	"names" : names_all
	}
	return render(request , "adminapp/loanform.html" , context)



@login_required(login_url="/")
def paid_form_view(request):
	names_all = all_names()
	names_all = set(names_all)

	formobj = PaidForm()
	context = {
	"form" : formobj,
	"names" : names_all
	}

	if request.method == "POST":

		formobj = PaidForm(request.POST)
		context = {
		"form" : formobj,
		"names" : names_all
		}

		if formobj.is_valid():
			
			name = request.POST.get("name")
			installment = request.POST.get("installment")

			paid_entry(name , int(installment))

			messages.info(request , "updated successfully !!!!!!!!!!!!!")
					
	formobj = PaidForm()
	context = {
	"form" : formobj,
	"names" : names_all
	}
	return render(request , "adminapp/paidform.html" , context)

@login_required(login_url="/")
def join_form_view(request):
	names_all = all_names()
	names_all = set(names_all)

	formobj = JoinForm()
	context = {
	"form" : formobj,
	"names" : names_all
	}

	if request.method == "POST":

		formobj = JoinForm(request.POST)
		context = {
		"form" : formobj,
		"names" : names_all
		}

		if formobj.is_valid():
			
			username = request.POST.get("Username")
			first = request.POST.get("FirstName")
			last = request.POST.get("LastName")
			password = request.POST.get("password")
			cd = request.POST.get("cd")

			user = User.objects.create_user(username = username , password=password)

			user.first_name = first.upper()
			user.last_name = last.upper()

			user.save()

			join_entry(f"{first.upper()} {last.upper()}" , int(cd))

			messages.info(request , f"{username} is joined successfully !!!!!!!!!!!!!")
					

	return render(request , "adminapp/joinform.html" , context)