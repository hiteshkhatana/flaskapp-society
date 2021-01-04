from django.db import models

# Create your models here.
class MonthInfo(models.Model):
	month = models.CharField(max_length = 50)
	interest = models.FloatField()
	cash_in_hand = models.IntegerField()
	loan_given = models.IntegerField()
	total_members = models.IntegerField()

	class Meta:
		db_table = "Month-info"

	def __str__(self):
		return self.month


class InterestShared(models.Model):
	name = models.CharField(max_length = 50)
	interest_collected = models.FloatField()
	paid = models.CharField(max_length = 10)

	class Meta:
		db_table = "Interest-shared"

	def __str__(self):
		return self.name

