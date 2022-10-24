from django.contrib import admin
from .models import proxyListModel
import requests, json
# Register your models here.

class proxyListAdmin(admin.ModelAdmin):
	list_display = ('id','list_name', 'country', 'region')
	list_display_links = ('id','list_name')
	def save_model(self, request, obj, form, change):
		res = requests.get(obj.link_api)
		obj.data = json.loads(res.text)
		super().save_model(request, obj, form, change)
admin.site.register(proxyListModel, proxyListAdmin)