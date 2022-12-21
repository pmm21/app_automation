import json, random, time, psutil

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import CPUInfoViewActive
from channels.db import database_sync_to_async


class CPUInfoConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = 'cpu_info'
		self.room_group_name = 'cpu_info_group'
		await self.accept()

		await self.channel_layer.group_add(
			self.room_group_name, self.channel_name
		)

		user = self.scope['user']
		if user.is_authenticated:
			await self.update_user_status(user,True)

	async def disconnect(self, close_code):
		user = self.scope['user']
		if user.is_authenticated:
			await self.update_user_status(user,False)

		await self.channel_layer.group_discard(
			self.room_group_name, self.channel_name
		)

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json["message"]

		await self.channel_layer.group_send(
			self.room_group_name, {"type": "chat_message", "message": message}
		)
	async def chat_message(self, event):
		message = event["message"]
		await self.send(text_data=json.dumps({"message": message}))

	@database_sync_to_async
	def update_user_status(self, user,status):
		return CPUInfoViewActive.objects.filter(user_id=user.pk).update(status=status)