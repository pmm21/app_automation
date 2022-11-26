from django.contrib import admin
from .models import proxyListModel, QClusterRunningTask
import requests, json
# Register your models here.
from django_q.tasks import async_task, Task

class proxyListAdmin(admin.ModelAdmin):
	list_display = ('id','list_name', 'country', 'region')
	list_display_links = ('id','list_name')
	def save_model(self, request, obj, form, change):
		res = requests.get(obj.link_api)
		obj.proxies = json.loads(res.text)
		super().save_model(request, obj, form, change)
admin.site.register(proxyListModel, proxyListAdmin)

class QClusterRunningTaskAdmin(admin.ModelAdmin):
	list_display = ('id','func', 'args','kwargs', 'started')

admin.site.register(QClusterRunningTask, QClusterRunningTaskAdmin)