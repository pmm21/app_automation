from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django_q.tasks import async_task, result, fetch

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
from .functions.gg_search import GG_SEARCH
from .functions.ggsr_desktop_structure import GGSR


class GGSearchAPIView(APIView):
	default_token = 'DsxfyqMzNcCQDrcY1B7WJFmYjBYadPRZJ5k81tCQA0NWCp1bfPSPhNTx5KwjEmHy'
	def get(self, request):
		return Response({'status':'oke'}, status=status.HTTP_200_OK)

	def post(self, request):
		data = request.data
		try:
			token = data['token']
			config = data['config']
			key_list = data['key_list']
		except:
			return Response({'error': 'error fields'}, status=status.HTTP_200_OK)

		if token == self.default_token:
			output = []
			async_task('app_gg_crawl.functions.gg_search.GG_SEARCH', key_list, config)
			output = {'status':'got your requests'}
		else:
			output = {'error':'Permission error'}

		return Response(output, status=status.HTTP_200_OK)

class GGSRStructure(APIView):
	default_token = 'DsxfyqMzNcCQDrcY1B7WJFmYjBYadPRZJ5k81tCQA0NWCp1bfPSPhNTx5KwjEmHy'
	def get(self, request):
		return Response({'status':'oke'}, status=status.HTTP_200_OK)

	def post(self, request):
		data = request.data
		try:
			token = data['token']
			html_text = data['html_text']
		except:
			return Response({'error': 'error fields'}, status=status.HTTP_200_OK)
		if token == self.default_token:
			output = GGSR(html_text).output_data
			output = {'output': output}
		else:
			output = {'error':'Permission error'}
		return Response(output, status=status.HTTP_200_OK)


class Test(View):
	def get(self, request):
		key_list = ['seo là gì', 'seo tphcm']
		config = {
			"proxy_country":"VN",
			"proxy_region":False,
			"driver_device":"DESKTOP",
			"driver_headless":True,
			"num100":True
		}
		output = GG_SEARCH(key_list, config).output
		return JsonResponse({'output':output})



import time
from django_q.models import Task
from .models import QClusterRunningTask
def test_process(project_id, *args, **kwargs):
	print('start process')
	print(args)
	print(kwargs)
	time.sleep(2)
	# all_task = Task.objects.all()
	# for task in all_task:
	# 	print(task.name, task.args, task.kwargs, type(task.args), type(task.kwargs))

	print('done process')
	return 'oke'

def test_hook(task):
	print('start hook')
	# print('results', task.result)
	print('done hook')

class TestCallBack(View):
	def get(self, request):
		project_id = 123124
		object_id = [1,23,123,31]
		key1 = None
		key2 = 'something'
		task_id = async_task('app_gg_crawl.views.test_process', project_id,object_id,key1=key1,key2=key2, hook='app_gg_crawl.tests.test_hook')

		QClusterRunningTask.task_create(task_id, '123', 'app_gg_crawl.views.test_process', project_id, object_id, key1=key1, key2=key2, hook='app_gg_crawl.tests.task_hook_delete')
		return JsonResponse({'status':'oke'})