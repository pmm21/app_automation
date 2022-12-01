from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django_q.tasks import async_task, result, fetch
from django_q.models import Task
from app_selenium.models import QClusterRunningTask

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
from .functions.gg_search import GG_SEARCH
from .functions.ggsr_desktop_structure import GGSR
import time

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
			output = {
				'error': 'error fields',
				'config':config, 
				'key_list':key_list
			}
			return Response(output, status=status.HTTP_200_OK)

		if token == self.default_token:
			if len(key_list)>6:
				output = {'error':'Just crawl maximum 6 keys in 1 request'}
			else:
				func = "app_gg_crawl.functions.gg_search.gg_search"
				task_id = async_task(func, key_list, config)
				time.sleep(3)
				task = Task.objects.filter(id=task_id)
				if task:
					if not task[0].success:
						output = {'error': task[0].result}
					else:
						output = task[0].result
				else:
					time.sleep(15+len(key_list)*2.5)
					while True:
						task = Task.objects.filter(id=task_id)
						if task:
							if task[0].success:
								output = task[0].result
							else:
								output = {'error': task[0].result}
							break
						time.sleep(2)
		else:
			output = {'error':'Permission error'}
		output['config'] = config
		output['key_list'] = key_list
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

from .functions.gasistant_requests import gasistant_recheck_market
class GKeySearchAPIView(APIView):
	default_token = 'DsxfyqMzNcCQDrcY1B7WJFmYjBYadPRZJ5k81tCQA0NWCp1bfPSPhNTx5KwjEmHy'
	def get(self, request):
		return Response({'status':'connect'}, status=status.HTTP_200_OK)

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
			# gasistant_recheck_market(key_list, config)
			func = "app_gg_crawl.functions.gasistant_requests.gasistant_recheck_market"

			task_id = async_task(func, key_list, config)
			QClusterRunningTask.task_create(task_id, func, str(key_list))
			output = {'status':'got your requests'}
		else:
			output = {'error':'Permission error'}

		return Response(output, status=status.HTTP_200_OK)