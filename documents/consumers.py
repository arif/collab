import json

from channels.generic.websocket import AsyncWebsocketConsumer

from documents.utils import serialize_user


class DocumentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']

        self.document_id = self.scope.get('url_route').get('kwargs').get('id')
        self.document_group_name = f'document_{self.document_id}'

        await self.channel_layer.group_add(
            self.document_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.document_group_name,
            {
                'type': 'viewer_join',
                'data': self.user,
            }
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.document_group_name,
            {
                'type': 'viewer_leave',
                'data': self.user,
            }
        )

        # Leave document group
        await self.channel_layer.group_discard(
            self.document_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        event_name = data.get('type', None)
        event_data = data.get('data', None)
        method = getattr(self, event_name, None)
        if method is not None:
            await method(event_data)
        else:
            pass

    async def viewer_join(self, event):
        data = event.get('data', None)
        print('viewer_join received', data)
        await self.send(text_data=json.dumps({
            'type': 'viewer_join',
            'data': serialize_user(data),
        }))

    async def viewer_leave(self, event):
        data = event.get('data', None)
        print('viewer_leave received', data)
        await self.send(text_data=json.dumps({
            'type': 'viewer_leave',
            'data': serialize_user(data),
        }))

    async def document_updated(self, event):
        title = event.get('title', '')
        content = event.get('content', '')
        data = {
            'title': title,
            'content': content,
        }
        print('document_updated received', data)
        await self.send(text_data=json.dumps({
            'type': 'document_updated',
            'data': data,
        }))
