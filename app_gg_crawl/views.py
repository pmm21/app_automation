from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django_q.tasks import async_task

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