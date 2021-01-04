from datetime import datetime
from members.models import Members
from .models import MonthInfo , InterestShared

from django.shortcuts import get_list_or_404 , get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q

def dates():
	date = datetime.now()
	month = date.strftime("%m")
	year = date.strftime("%Y")
	cur_month = f"{int(month)}-{year}"


	if int(month) == 12:
		next_month = f"1-{int(year)+1}"
	else:
		next_month = f"{int(month)+1}-{year}"
	if int(month) == 1:
		prev_month = f"12-{int(year)-1}"
	else:
		prev_month = f"{int(month)-1}-{year}"

	return cur_month , next_month , prev_month

cur_month , next_month , prev_month = dates()

def onemonth_record(month):
	objlist = get_list_or_404(Members , month = month)
	return objlist

def all_months():
	objlist = Members.objects.values_list('month', flat = True)

	return set(objlist)

def all_names():
	objs = Members.objects.filter(month = next_month)
	names_all = objs.values_list('name' , flat = True)
	return set(names_all)

def all_users():

	User = get_user_model()
	users = User.objects.values_list('username' , flat = True)

	return users

def total_cd(name):
	
	person_record = Members.objects.filter(name = name )
	all_cds = person_record.values_list('cd' , flat = True)

	return sum(list(all_cds)[:-1])

def month_updates(month):
	
	objs = Members.objects.filter(month = month)
	cds = objs.values_list('cd' , flat = True)
	installments = objs.values_list('installment' , flat = True)
	interests = objs.values_list('interest' , flat = True)
	totals = objs.values_list('total' , flat = True)
	loanbals = objs.values_list('loan_bal' , flat = True)
	
	objs = Members.objects.filter(~Q(month = next_month))
	total_interest = objs.values_list('interest' , flat = True)

	return sum(list(cds)) , sum(list(installments)) , sum(list(interests)) , sum(list(totals)) , sum(list(loanbals)) , sum(list(total_interest))



def add_next_month():
	objlist = Members.objects.values_list('month', flat = True)
	if next_month not in objlist:
		present_data = get_list_or_404(Members , month = cur_month)

		for row in present_data:
			new_loan_bal = row.loan_bal - row.installment
			new_interest = new_loan_bal*0.005
			new_total =  row.cd + row.installment + new_interest
			Members.objects.create(serial = row.serial , name = row.name,cd = row.cd,installment = row.installment,interest = new_interest,total = new_total,loan_bal = new_loan_bal, month = next_month )

		monthinfo_cal()

def loan_entry(name , amount , installment):
	person_record = get_object_or_404(Members , name = name , month = next_month)
	person_record.installment += installment
	person_record.loan_bal += amount
	person_record.total = person_record.cd + person_record.installment + person_record.loan_bal*0.005
	person_record.save()


	monthobj = get_object_or_404(MonthInfo , month = cur_month)
	monthobj.loan_given += amount
	monthobj.cash_in_hand -= amount
	monthobj.save()

def remove_entry(name):
	removeobj = get_object_or_404(Members , name = name , month = next_month)
	removeobj.delete()



def join_entry(name , cd ):
	all_serials = Members.objects.values_list('serial' , flat = True)
	new_serial = max(set(all_serials)) + 1
	Members.objects.create(serial = new_serial ,name = name,cd = cd,installment = 0,interest = 0.0,total = cd ,loan_bal = 0, month = cur_month )
	Members.objects.create(serial = new_serial ,name = name,cd = 1000,installment = 0,interest = 0.0,total = 1000 ,loan_bal = 0, month = next_month )

	InterestShared.objects.create(name = name , interest_collected = 0 , paid = "No")

	monthobj = get_object_or_404(MonthInfo , month = cur_month)

	monthobj.cash_in_hand += cd
	monthobj.save()


def paid_entry(name , installment):
	record_nm = get_object_or_404(Members , name = name , month = next_month)

	record_nm.loan_bal += ( record_nm.installment - installment )
	record_nm.interest = record_nm.loan_bal*0.005
	record_nm.total = record_nm.cd + record_nm.installment + record_nm.interest
	record_nm.save()

	record = get_object_or_404(Members , name = name , month = cur_month)
	record.total -= (record.installment-installment)
	record.installment = installment
	record.save()

	monthobj = get_object_or_404(MonthInfo , month = cur_month)
	monthobj.cash_in_hand -= (record_nm.installment - installment)
	monthobj.save()


def monthinfo_cal():
	# calculating total interest of current month
	objlist = Members.objects.filter(month = cur_month)
	total_interest = objlist.values_list('interest',flat = True)
	total_interest = sum(list(total_interest))

	# calculating total members of current month
	names = objlist.values_list('name' , flat = True)
	total_members = len(names)

	# Adding new field in MonthInfo 
	MonthInfo.objects.create(month = cur_month , interest = total_interest , cash_in_hand = 0 ,loan_given = 0 , total_members = total_members )

	# selecting members to distribute interest collected
	selected_members = InterestShared.objects.filter(paid = "No")
	# selected_members = get_list_or_404(InterestShared , paid = "No")

	# adding shares in members record
	for memb in selected_members:
		memb.interest_collected +=  (total_interest/total_members)
		memb.save()

	# calculating cash in hand
	cash_in_hand_cal()


def cash_in_hand_cal():
	# Total interest shared this month
	interest_given_to = InterestShared.objects.filter(paid = cur_month)
	given = interest_given_to.values_list('interest_collected' , flat = True)
	interest_given = sum(list(given))
	

	objlist = Members.objects.filter(month = cur_month)

	total_cd = objlist.values_list('cd' ,flat = True)
	total_installment = objlist.values_list('installment' ,flat = True)

	prev_cash_obj = get_object_or_404(MonthInfo , month = prev_month)


	obj = get_object_or_404(MonthInfo , month = cur_month)

	obj.cash_in_hand = prev_cash_obj.cash_in_hand + sum(list(total_cd)) + sum(list(total_installment)) + obj.loan_given - interest_given
	obj.save()










