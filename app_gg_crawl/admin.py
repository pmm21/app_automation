from django.contrib import admin
from .models import TestGGSearchModel, TestSaveData
from .functions.gasistant_requests import gasistant_recheck_market
from app_selenium.models import QClusterRunningTask
from django_q.tasks import async_task, Task
# Register your models here.

class TestGGSearchAdmin(admin.ModelAdmin):
	readonly_fields = ('key_data',)
	def save_model(self, request, obj, form, change):
		key_list = [item.strip() for item in obj.key_list.split('\n')]
		config = {
			'num100':False,
			'driver_headless':False
		}
		func = "app_gg_crawl.functions.gasistant_requests.gasistant_recheck_market"
		task_id = async_task(func,key_list, config)
		QClusterRunningTask.task_create(task_id, func=func)
		super().save_model(request, obj, form, change)

admin.site.register(TestGGSearchModel, TestGGSearchAdmin)
admin.site.register(TestSaveData)