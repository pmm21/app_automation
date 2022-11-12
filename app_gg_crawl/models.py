from django.db import models
from picklefield import PickledObjectField

# Create your models here.

class QClusterRunningTask(models.Model):
	id = models.CharField(max_length=32, primary_key=True, editable=False)
	func = models.CharField(max_length=256)
	hook = models.CharField(max_length=256, null=True)
	args = PickledObjectField(null=True)
	kwargs = PickledObjectField(null=True)
	user_id = models.CharField(max_length=256)
	started = models.DateTimeField(auto_now_add=True)

	def task_create(task_id, user_id, func, *args, **kwargs):
		new_task = QClusterRunningTask(
				id = task_id,
				func = func,
				user_id = user_id,
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

def task_hook_delete(task):
	print('start hook')
	# r_tasks = QClusterRunningTask.objects.all()
	# tasks = Task.objects.all()
	# for item in r_tasks:
	# 	print(item.id)
	# 	if tasks.filter(id=item.id):
	# 		try:
	# 			item.delete()
	# 		except:
	# 			pass
def test_hook(task):
	print('start hook')
	# print('results', task.result)
	print('done hook')