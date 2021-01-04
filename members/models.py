from django.db import models
from django.urls import reverse

# Create your models here.
class Members(models.Model):
	serial = models.IntegerField()
	name = models.CharField(max_length=100)
	cd = models.IntegerField()
	installment = models.IntegerField()
	interest = models.FloatField()
	total = models.FloatField()
	loan_bal = models.FloatField()
	month = models.CharField(max_length=10)

	class Meta:
		db_table = "complete"

	def __str__(self):
		return f"{self.month} {self.name}"
