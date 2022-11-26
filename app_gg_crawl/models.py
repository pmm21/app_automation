from django.db import models

# Create your models here.

class TestGGSearchModel(models.Model):
	test_name = models.CharField(max_length=100)
	key_list = models.TextField()
	key_data = models.JSONField(null=True)

	class Meta:
		verbose_name = ("Test GG search")
	def __str__(self):
		return self.test_name



class TestSaveData(models.Model):
	url = models.CharField(max_length=125)
	data = models.JSONField()

	class Meta:
		verbose_name = ("Save Data")
	def __str__(self):
		return self.url