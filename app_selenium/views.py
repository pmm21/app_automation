from django.shortcuts import render
from django.http import JsonResponse
from django.views import View


from .functions.proxy_manage import get_proxy
# from .functions.cpu_info import RunCpuInfo
class TestView(View):
	def get(self, request):
		get_proxy()
		return JsonResponse({'RUNING_PROXY':'RUNING_PROXY'})



def CPUInfoView(request):
	return render(request, "app_selenium/cpu_info.html")

# def cpuinfoviewactivate(request):
# 	RunCpuInfo()
# 	return JsonResponse({'status':'oke'})