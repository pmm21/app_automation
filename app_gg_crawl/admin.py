from django.contrib import admin
from .models import QClusterRunningTask, TestGGSearchModel, TestSaveData
from .functions.gasistant_requests import gasistant_recheck_market
from django_q.tasks import async_task, result, fetch
# Register your models here.
class QClusterRunningTaskAdmin(admin.ModelAdmin):
	list_display = ('id','func', 'args','kwargs', 'hook', 'started')
admin.site.register(QClusterRunningTask, QClusterRunningTaskAdmin)

class TestGGSearchAdmin(admin.ModelAdmin):
	readonly_fields = ('key_data',)
	def save_model(self, request, obj, form, change):
		key_list = [item.strip() for item in obj.key_list.split('\n')]
		config = {
			'num100':False,
			'driver_headless':False
		}
		async_task("app_gg_crawl.functions.gasistant_requests.gasistant_recheck_market",key_list, config)
		super().save_model(request, obj, form, change)

admin.site.register(TestGGSearchModel, TestGGSearchAdmin)
admin.site.register(TestSaveData)