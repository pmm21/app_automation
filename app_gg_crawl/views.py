from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
from .functions.gg_search import GG_SEARCH


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
			output = GG_SEARCH(key_list, config).output
		else:
			output = {'error':'Permission error'}

		return Response(output, status=status.HTTP_200_OK)
