from django.db import models

# Create your models here.
COUNTRIES = [('VN','Việt Nam'), ('USA','Hoa Kỳ')]
class proxyListModel(models.Model):
	defaut_dict = dict({'data':[]})
	list_name = models.CharField(max_length=125)
	country = models.CharField(max_length=125, choices=COUNTRIES)
	region = models.CharField(max_length=125, blank=True, null=True)
	link_api = models.CharField(max_length=500, blank=True, null=True)
	proxies = models.JSONField(null=True, blank=True)
	running_proxies = models.JSONField(default=defaut_dict)
	dead_proxies = models.JSONField(default=defaut_dict)

	class Meta:
		verbose_name = ("Proxy List")
	def __str__(self):
		return self.list_name

# class SeleniumTesterModel(models.Model):
# 	url = models.CharField(max_length=250)
# 	class Meta:
# 		verbose_name = ("Proxy List")
# 	def __str__(self):
# 		return self.url
# class Xpath(models.Model):
# 	xpath = models.CharField(max_length=250)
# 	of_url = models.ForeignKey(SeleniumTesterModel, on_delete=models.CASCADE)
