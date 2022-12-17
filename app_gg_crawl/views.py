from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django_q.tasks import async_task, result, fetch
from django_q.models import Task

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
from .functions.gg_search import GG_SEARCH, gg_search, c_config
from .functions.ggsr_desktop_structure import GGSR
import time

class CheckQclusterStatus(View):
	default_token = 'DsxfyqMzNcCQDrcY1B7WJFmYjBYadPRZJ5k81tCQA0NWCp1bfPSPhNTx5KwjEmHy'
	def get(self, request):
		
		token = request.GET.get('token')
		task_id = request.GET.get('task_id')
		print(task_id, token)
		if token== '' or task_id == '':
			output = {
				'status': 'error fields',
			}
			return JsonResponse(output)
		if token!= self.default_token:
			output = {
				'status': 'error: You don\'t have permission',
				'token':token,
				'task_id':task_id
			}
			return JsonResponse(output)
		else:
			task = Task.objects.filter(id=task_id)
			print(task)
			if task:
				task = task[0]
				output = {
					'status': 'success' if task.success else 'fails',
					'result': task.result
				}
			else:
				output = {
					'status': 'running',
					'result': ''
				}
			return JsonResponse(output)

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
				'data':data
			}
			return Response(output, status=status.HTTP_400_BAD_REQUEST)

		r_status=status.HTTP_200_OK
		if token == self.default_token:
			if len(key_list)>6:
				output = {'error':'Just crawl maximum 6 keys in 1 request'}
				r_status=status.HTTP_400_BAD_REQUEST
			else:
				func = "app_gg_crawl.functions.gg_search.gg_search"
				task_id = async_task(func, key_list, config)
				time.sleep(3)
				task = Task.objects.filter(id=task_id)
				if task:
					if task[0].success:
						output = task[0].result
					else:
						output = {'error': task[0].result}
						r_status=status.HTTP_500_INTERNAL_SERVER_ERROR
				else:
					time.sleep(20+len(key_list)*10)
					while True:
						task = Task.objects.filter(id=task_id)
						if task:
							if task[0].success:
								output = task[0].result
							else:
								output = {'error': task[0].result}
								r_status=status.HTTP_500_INTERNAL_SERVER_ERROR
							break
						time.sleep(2)
		else:
			output = {'error':'Permission error'}
			r_status=status.HTTP_403_FORBIDDEN

		return Response(output, status=r_status)


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
			# gasistant_recheck_market(key_list, config)
			try:
				if config['num100']==True:
					func = "app_gg_crawl.functions.gasistant_requests.gasistant_recheck_ranking"
				else:
					func = "app_gg_crawl.functions.gasistant_requests.gasistant_recheck_market"
			except:
				func = "app_gg_crawl.functions.gasistant_requests.gasistant_recheck_market"
			task_id = async_task(func, key_list, config)
			output = {'status':'got your requests', 'task_id':task_id}
		else:
			output = {'error':'Permission error'}

		return Response(output, status=status.HTTP_200_OK)


class TestGGSearch(APIView):
	default_token = 'DsxfyqMzNcCQDrcY1B7WJFmYjBYadPRZJ5k81tCQA0NWCp1bfPSPhNTx5KwjEmHy'
	def get(self, request):
		return Response({'status':'oke'}, status=status.HTTP_200_OK)

	def post(self, request):
		data = request.data
		print(data)
		try:
			token = data['token']
			config = data['config']
			key_list = data['key_list']
		except:
			output = {
				'error': 'error fields',
				'data':data
			}
			return Response(output, status=status.HTTP_400_BAD_REQUEST)

		r_status=status.HTTP_200_OK
		if token == self.default_token:
			config = c_config(config)
			output = GG_SEARCH(key_list, config).output
		else:
			output = {'error':'Permission error'}
			r_status=status.HTTP_403_FORBIDDEN

		return Response(output, status=r_status)