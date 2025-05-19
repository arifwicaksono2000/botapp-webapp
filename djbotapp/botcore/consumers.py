from channels.generic.websocket import AsyncWebsocketConsumer
import json

class BotStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("bot_status", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("bot_status", self.channel_name)

    async def send_status(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    async def send_position_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))


