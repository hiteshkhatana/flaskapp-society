from datetime import datetime
import warnings
import mysql.connector
warnings.filterwarnings("ignore")

class Prepare:
	def __init__(self):
		self.db = mysql.connector.connect(host="us-cdbr-east-02.cleardb.com",user="b493015757bb60",password="161ce573",database = "heroku_1d4de87686e22e0")
		# self.db = mysql.connector.connect(host="localhost",user="root",password="hitesh1454",database = "commitee")		
		self.cur = self.db.cursor(buffered = True)

		date = datetime.now()
		self.month = date.strftime("%m")
		self.year = date.strftime("%Y")
		self.cur_month = f"{int(self.month)}/{self.year}"

		#getting next month
		if int(self.month) == 12:
			self.next_month = f"1/{int(self.year)+1}"
		else:
			self.next_month = f"{int(self.month)+1}/{self.year}"
		if int(self.month) == 1:
			self.prev_month = f"12/{int(self.year)-1}"
		else:
			self.prev_month = f"{int(self.month)-1}/{self.year}"



class Check(Prepare):
	def __init__(self ):
		super().__init__()

	def individual(self , name):
		#checking individual record 
		self.cur.execute("SELECT ID,NAME,CD,INSTALLMENT,INTEREST,TOTAL,BAL,MONTH FROM complete WHERE NAME = %s" , (name,))
		values = self.cur.fetchall()
		res = list(values)
		return res

	def all_names(self):
		self.cur.execute("SELECT DISTINCT(NAME) FROM complete")
		res = []
		for i in self.cur:
			res.append(i)
		return res

	def all_months(self):
		self.cur.execute("SELECT DISTINCT(MONTH) FROM complete")
		res = []
		for i in self.cur:
			res.append(i)
		return res

	def complete(self, month):
		#printing complete data
		self.cur.execute("SELECT ID,NAME,CD,INSTALLMENT,INTEREST,TOTAL,BAL,MONTH FROM complete WHERE MONTH = %s",(month,))
		res = []
		for i in self.cur:
			res.append(list(i))
		return res

	def show_interest_per_person(self):
		Update()
		self.cur.execute("SELECT NAME,INTEREST,PAID FROM interest_shared")
		res = []
		for i in self.cur:
			res.append(list(i))
		return res

	def monthly_updates(self,month):
		self.cur.execute("SELECT INTEREST,IN_HAND,MEMBERS FROM monthly_interest WHERE MONTH = %s",(month,))
		shared = self.cur.fetchall()
		self.cur.execute("SELECT SUM(BAL) FROM complete WHERE MONTH = %s",(month,))
		bal = self.cur.fetchone()
		if shared == None or shared == []:
			return None
		else:
			print(month,shared[0][0],bal[0],shared[0][1],shared[0][2])
			return [month,shared[0][0],float(bal[0]),shared[0][1],shared[0][2]]


class Update(Prepare):
	def __init__(self ):
		super().__init__()

		#preparing next month data
		self.cur.execute("SELECT MONTH FROM complete WHERE MONTH = %s" , (self.next_month,))
		ans = self.cur.fetchall()
		if ans == [] or ans == None:
			self.cur.execute("SELECT ID,NAME,CD,INSTALLMENT,INTEREST,TOTAL,BAL FROM  complete WHERE MONTH = %s",(self.cur_month,))
			data = self.cur.fetchall()
			new = []
			for i in data:
				i = list(i)
				i.insert(len(i),self.next_month)
				i = tuple(i) 
				new.append(i)
			self.cur.executemany("INSERT INTO complete values (%s,%s,%s,%s,%s,%s,%s,%s)",new)

			self.cur.execute("UPDATE complete SET BAL = BAL - INSTALLMENT,INTEREST = BAL*0.05,TOTAL = CD + INSTALLMENT + INTEREST WHERE MONTH = %s" , (self.next_month,))

			# self.cur.execute("INSERT INTO monthly_interest VALUES(%s,%s,%s,%s,%s)",(self.next_month,0,0,0,0))
			self.db.commit()



		self.cur.execute("SELECT MONTH FROM monthly_interest WHERE MONTH = %s" ,(self.cur_month,))
		ans = self.cur.fetchone()
		if ans == None or ans == []:
			self.total_interest_collected()
			try:
				self.cash_in_hand()
			except:
				pass

		self.cur.execute("SELECT MONTH FROM interest_shared WHERE MONTH = %s" ,(self.cur_month,))
		ans = self.cur.fetchone()
		if ans == None or ans == []:
			self.interest_per_person()

		


		# someone taken loan
	def loan_taken(self ,name , amount , install):
		
		self.cur.execute("UPDATE complete SET INSTALLMENT = INSTALLMENT + %s,BAL = BAL + %s,INTEREST = BAL*0.05,TOTAL = CD + INSTALLMENT + INTEREST WHERE NAME = %s and MONTH = %s", (install,amount,name,self.next_month))
		self.db.commit()

		
		self.cur.execute("UPDATE monthly_interest SET LOAN_GIVEN = LOAN_GIVEN + %s , IN_HAND = IN_HAND - %s WHERE MONTH = %s", (amount,amount,self.cur_month))
		self.db.commit()
		
		

		#someone wants to leave the commitee
	def leave(self , name):
		self.cur.execute("DELETE FROM complete WHERE NAME = %s AND MONTH = %s" , (name,self.next_month))
		self.db.commit()

		#someone wants to join the committe
	def join(self,name,cd):
		self.cur.execute("SELECT * FROM complete WHERE MONTH = %s AND NAME = %s",(self.cur_month,name))
		all_names = self.cur.fetchone()
		if all_names != None:
			return False
		self.cur.execute("SELECT COUNT(DISTINCT(ID)) FROM complete")
		ans = self.cur.fetchone()
		self.cur.execute("INSERT INTO complete(ID,NAME,CD,INSTALLMENT,INTEREST,TOTAL,BAL,MONTH) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)" ,(ans[0]+1,name , cd , 0 , 0 , 1000 , 0 , self.cur_month) )
		self.cur.execute("INSERT INTO complete(ID,NAME,CD,INSTALLMENT,INTEREST,TOTAL,BAL,MONTH) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)" ,(ans[0]+1,name , 1000 , 0 , 0 , 1000 , 0 , self.next_month) )
		self.cur.execute("UPDATE monthly_interest SET IN_HAND = IN_HAND + %s , MEMBERS = MEMBERS + 1 WHERE MONTH = %s",(cd,self.cur_month) )
		self.db.commit()

		#someone have paid the loan installment of this month
	def paid(self,name,installment_given):
		self.cur.execute("SELECT BAL FROM complete WHERE NAME = %s AND MONTH = %s",(name,self.cur_month))
		bal = self.cur.fetchone()
		self.cur.execute("UPDATE complete SET BAL = %s-%s,INTEREST = BAL*0.05,TOTAL = CD + INSTALLMENT + INTEREST WHERE NAME = %s AND MONTH = %s" , (int(bal[0]) ,int(installment_given),name,self.next_month))
		self.cur.execute("UPDATE complete SET INSTALLMENT = %s WHERE NAME = %s AND MONTH = %s",(int(installment_given),name,self.cur_month))
		self.cur.execute("SELECT INSTALLMENT FROM complete WHERE NAME = %s AND MONTH = %s",(name,self.cur_month))
		ans = self.cur.fetchone()
		self.cur.execute("UPDATE monthly_interest SET IN_HAND = IN_HAND-(%s-%s) WHERE MONTH = %s",(ans[0],installment_given,self.cur_month) )
		self.db.commit()


	def mannual(self,i_d,name,cd,installment,interest,total,loan,month):
		self.cur.execute("UPDATE complete SET ID = %s, CD = %s,INSTALLMENT = %s,INTEREST = %s,TOTAL = %s,BAL = %s WHERE NAME = %s AND MONTH = %s" , (i_d,cd,installment,interest,total,loan,name,month))

		self.cur.execute("SELECT SUM(INTEREST) , COUNT(NAME) FROM complete WHERE MONTH = %s" , (month,))
		ans = self.cur.fetchone()
		self.cur.execute("UPDATE monthly_interest SET INTEREST = %s , MEMBERS = %s WHERE MONTH = %s",(ans[0],ans[1],month))

		self.cur.execute("SELECT DISTINCT NAME FROM complete WHERE MONTH = %s" , (self.cur_month,))
		names = self.cur.fetchall()

		self.cur.execute("SELECT INTEREST/MEMBERS FROM monthly_interest WHERE MONTH = %s" , (self.cur_month,))
		p_int = self.cur.fetchone()[0]
		
		for name in names:
			self.cur.execute("SELECT INTEREST FROM interest_shared WHERE NAME = %s AND MONTH = %s",(name[0],self.prev_month))
			ans = self.cur.fetchone()
			if ans == None or ans == []:
				ans = 0
			else:
				ans = ans[0]
			
			self.cur.execute("UPDATE interest_shared SET INTEREST =%s, PAID = %s WHERE NAME = %s AND MONTH = %s" , (p_int,None,name[0],month))
		self.db.commit()

		self.cash_in_hand()

		#function for preparing total interest collection
	def total_interest_collected(self):
		self.cur.execute("SELECT SUM(INTEREST) , COUNT(NAME) FROM complete WHERE MONTH = %s" , (self.cur_month,))
		ans = self.cur.fetchone()
		print(ans)
		self.cur.execute("INSERT INTO monthly_interest(MONTH,INTEREST,MEMBERS) VALUES (%s,%s,%s)",(self.cur_month,ans[0],ans[1]))
		self.db.commit()

		#calculating interest collected per person
	def interest_per_person(self):
		self.cur.execute("SELECT DISTINCT NAME FROM complete WHERE MONTH = %s" , (self.cur_month,))
		names = self.cur.fetchall()
		self.cur.execute("SELECT INTEREST/MEMBERS FROM monthly_interest WHERE MONTH = %s" , (self.cur_month,))
		p_int = self.cur.fetchone()[0]
		for name in names:
			self.cur.execute("SELECT INTEREST FROM interest_shared WHERE NAME = %s AND MONTH = %s",(name[0],self.prev_month))
			ans = self.cur.fetchone()
			if ans == None or ans == []:
				ans = 0
			else:
				ans = ans[0]
			
			self.cur.execute("INSERT INTO interest_shared VALUES(%s,%s,%s,%s)" , (name[0],p_int+ans,None,self.cur_month))
			# self.cur.execute("UPDATE interest_shared SET INTEREST = %s WHERE NAME = %s" , (float(p_int)+float(ans),name[0]))


		self.db.commit()
		
		


	def cash_in_hand(self):
		self.cur.execute("SELECT SUM(INTEREST) FROM interest_shared WHERE PAID = %s",(self.cur_month,))
		shared = self.cur.fetchone()
		if shared[0] == None:
			shared = 0
		else:
			shared = shared[0]
		self.cur.execute("SELECT LOAN_GIVEN FROM monthly_interest WHERE MONTH = %s",(self.cur_month,))
		loan_given = self.cur.fetchone()
		if loan_given == None or loan_given == []:
			loan_given = 0
		else:
			loan_given = loan_given[0]
		self.cur.execute("SELECT IN_HAND FROM monthly_interest WHERE MONTH = %s",(self.prev_month,))
		in_hand_p = self.cur.fetchone()
		self.cur.execute("SELECT sum(CD)+sum(INSTALLMENT),COUNT(NAME) FROM complete WHERE MONTH = %s",(self.cur_month,))
		ans = self.cur.fetchone()
		collection = ans[0]
		members = ans[1]
		total = collection + in_hand_p[0] - shared

		in_hand_n = total - loan_given
		self.cur.execute("UPDATE monthly_interest SET MEMBERS = %s ,IN_HAND = %s WHERE MONTH = %s",(members,in_hand_n,self.cur_month))
		self.db.commit()


if __name__ == "__main__":
	pass
	





		
