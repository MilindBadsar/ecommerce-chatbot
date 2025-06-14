from django.db import models

class ChatInteraction(models.Model):
    session_id = models.CharField(max_length=255, db_index=True, help_text="Unique identifier for the chat session.")
    user_message = models.TextField(help_text="The message sent by the user.")
    bot_response = models.TextField(help_text="The response generated by the chatbot.")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="The time of the interaction.")

    class Meta:
        ordering = ['timestamp']
        verbose_name = "Chat Interaction"
        verbose_name_plural = "Chat Interactions"

    def __str__(self):
        return f"Session {self.session_id}: User: '{self.user_message[:50]}...' Bot: '{self.bot_response[:50]}...'"