from django.contrib import admin
from .models import QClusterRunningTask

# Register your models here.
class QClusterRunningTaskAdmin(admin.ModelAdmin):
	list_display = ('id','func', 'user_id', 'args','kwargs', 'hook', 'started')
admin.site.register(QClusterRunningTask, QClusterRunningTaskAdmin)