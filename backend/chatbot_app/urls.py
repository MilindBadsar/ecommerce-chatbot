from django.urls import path
from .views import ChatbotAPIView

urlpatterns = [
    path('chat/', ChatbotAPIView.as_view(), name='chatbot-api'),
    # can add paths for retrieving chat history here if needed later
    # path('chat/history/<str:session_id>/', ChatInteractionListView.as_view(), name='chat-history'),
]