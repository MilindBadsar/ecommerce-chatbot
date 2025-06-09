from rest_framework import serializers
from .models import ChatInteraction

class ChatInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatInteraction
        fields = ['id', 'session_id', 'user_message', 'bot_response', 'timestamp']
        read_only_fields = ['timestamp'] # Timestamp is auto-generated