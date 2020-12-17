from flask import Flask, request, jsonify ,render_template,request,redirect,url_for
from comm import Prepare , Check , Update


app = Flask(__name__)



@app.route('/')
def myApp():
	Prepare()
	Update()
	return render_template("dashboard.html")

@app.route("/names")
def al_names():
	names = Check().all_names()
	response = jsonify(names)
	return response

@app.route("/months")
def al_months():
	names = Check().all_months()
	response = jsonify(names)
	return response


@app.route("/individualdata",methods=["POST"])
def individual_data():
	name = request.form["name"]
	res = Check().individual(name)
	response = jsonify(res)
	return response

@app.route("/monthdata",methods=["POST"])
def month_data():
	c = Check()
	month = request.form["month"]
	res = c.complete(month)
	res2 = c.monthly_updates(month)
	response = jsonify({"complete" : res , "updates" : res2})
	return response


@app.route("/adminpage" , methods=["POST"])
def admin_page():
	user = request.form["username"]
	paswd = request.form["password"]
	if #username and password Authentication succeeds:
		return render_template("admin.html")
	else:
		return render_template("dashboard.html",msg = "failed!! You have entered wrong username and password")
 	
@app.route('/joinpage',methods=["POST"])
def join_us():
	name = request.form["name"]
	cd = request.form["cd"]
	Update().join(name,cd)
	response = jsonify(["success"])
	return response

@app.route('/leavepage',methods=["POST"])
def leave_us():
	name = request.form["name"]
	Update().leave(name)
	response = jsonify(["success"])
	return response

@app.route('/paidpage',methods=["POST"])
def paid_install():
	name = request.form["name"]
	installment = request.form["installment"]
	Update().paid(name,installment)
	response = jsonify(["success"])
	return response

@app.route('/loanpage',methods=["POST"])
def loan_taken():
	name = request.form["name"]
	amount = request.form["amount"]
	installment = request.form["installment"]
	Update().loan_taken(name,amount,installment)
	response = jsonify(["success"])
	return response

@app.route('/editpage',methods=["POST"])
def edit_record():
	i_d = request.form["id"]
	name = request.form["name"]
	cd = request.form["cd"]
	installment = request.form["installment"]
	interest = request.form["interest"]
	total = request.form["total"]
	loan = request.form["loan"]
	month = request.form["month"]
	Update().mannual(i_d,name,cd,installment,interest,total,loan,month)
	response = jsonify(["success"])
	return response


if __name__ == '__main__':
    app.run(debug = True, port = 5000)
