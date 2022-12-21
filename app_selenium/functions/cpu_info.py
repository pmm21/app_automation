from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import platform
import time, psutil
# from django_q.tasks import async_task

from ..models import CPUInfoViewActive
def get_cpu_info():
	if platform.system()=='Windows':
		name = 'firefox.exe'
	else:
		name = 'firefox'
	return  {
			'firefox_count':len([poc for poc in psutil.process_iter(['pid', 'name']) if poc.info['name']==name]),
			'ram_percent':psutil.virtual_memory().percent,
			'cpu_percent':psutil.cpu_percent()
		}

def RunCpuInfo():
	channel_layer = get_channel_layer()
	time.sleep(10)
	while True:
		if CPUInfoViewActive.objects.filter(status=True):
			async_to_sync(channel_layer.group_send)("cpu_info_group", {
			    "type": "chat.message",
			    "message": get_cpu_info(),
			})
		time.sleep(1)

fun= "app_selenium.functions.cpu_info.RunCpuInfo"
# async_task(func)

