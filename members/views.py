from django.shortcuts import render , get_object_or_404 , get_list_or_404
from django.contrib.auth.decorators import login_required

from .models import Members


# Create your views here.
@login_required(login_url="/")
def onemember_record(request , name):
	objlist = get_list_or_404(Members , name  = name)
	objlist = objlist[::-1]
	
	cd = totalcd(objlist)

	next_pay = next_month_pay(objlist)

	last_loanmonth = loan_last_month(objlist)

	context = {
	"objectlist" : objlist[1:],
	"user":name,
	"totalcd" : cd,
	"nextpay" : next_pay,
	"loan_end" : last_loanmonth
	}

	return render(request , "members/one_member_record.html" , context)

def totalcd(record):
	total_cd = 0
	for i in record[1:]:
		total_cd += i.cd

	return total_cd

def next_month_pay(record):
	nextmonthpay = record[0].total
	return nextmonthpay

def loan_last_month(record):
	bal = record[0].loan_bal
	install = record[0].installment
	month = record[0].month
	mon , yr = month.split("-")

	if bal == 0:
		return None

	no_of_months = round(bal/install)


	if int(no_of_months) + int(mon) <= 12:
		end_month = f"{int(mon)+int(no_of_months)}-{yr}"


	year = 0
	while no_of_months > 12:
		no_of_months -= 12
		year += 1
		end_month = f"{no_of_months}-{int(yr)+int(year)}"
		
	

	return end_month



