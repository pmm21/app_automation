from django.db import models
from picklefield import PickledObjectField

# Create your models here.

class TestGGSearchModel(models.Model):
	test_name = models.CharField(max_length=100)
	key_list = models.TextField()
	key_data = models.JSONField(null=True)

	class Meta:
		verbose_name = ("Test GG search")
	def __str__(self):
		return self.test_name

class QClusterRunningTask(models.Model):
	id = models.CharField(max_length=32, primary_key=True, editable=False)
	func = models.CharField(max_length=256)
	hook = models.CharField(max_length=256, null=True)
	args = PickledObjectField(null=True)
	kwargs = PickledObjectField(null=True)
	started = models.DateTimeField(auto_now_add=True)

	def task_create(task_id, func, *args, **kwargs):
		new_task = QClusterRunningTask(
				id = task_id,
				func = func,
				args = args
			)
		try: 
			new_task.hook = kwargs['hook']
			kwargs.pop("hook")
			new_task.kwargs = kwargs
		except:
			new_task.hook = None
			new_task.kwargs = kwargs
		new_task.save()


class TestSaveData(models.Model):
	url = models.CharField(max_length=125)
	data = models.JSONField()

	class Meta:
		verbose_name = ("Save Data")
	def __str__(self):
		return self.url