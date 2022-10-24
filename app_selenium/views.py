from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from .functions.proxy_manage import get_proxy
class TestView(View):
	def get(self, request):
		get_proxy()
		return JsonResponse({'RUNING_PROXY':'RUNING_PROXY'})
