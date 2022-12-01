from django.contrib import admin
from .models import TestGGSearchModel, TestSaveData
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
		func = "app_gg_crawl.functions.gg_search.gg_search"
		task_id = async_task(func, key_list, config)
		super().save_model(request, obj, form, change)

admin.site.register(TestGGSearchModel, TestGGSearchAdmin)
admin.site.register(TestSaveData)