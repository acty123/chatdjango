# chat/consumers.py
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message
from person.models import LoggedInUser
import json, time

User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    # load messages
    def fetch_messages(self, data):
        messages = Message.last_10_message()
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)
    
    # show new message and save
    def new_message(self, data):
        session_active = self.scope['session'].session_key
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        log = LoggedInUser.objects.filter(user=author_user)[0]
        # not send if user doesn't have session or message is void
        if(data['message'] == "" or session_active != log.session_key):
            return True
        message = Message.objects.create(
            author=author_user, 
            content=data['message'])
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result[::-1]

    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str( message.timestamp.strftime("%m/%d/%Y, %I:%M:%S %p"))
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self,data)

    # Send the new messages
    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    # send the previous messages
    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        session_active = self.scope['session'].session_key
        author_user = User.objects.filter(username=self.scope['user'])[0]
        log = LoggedInUser.objects.filter(user=author_user)[0]
        # not send if user doesn't have session
        if session_active != log.session_key:
            return True

        message = event['message']
        self.send(text_data=json.dumps(message)) 