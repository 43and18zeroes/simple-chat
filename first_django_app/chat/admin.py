from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    fields = ('text', 'created_at', 'author', 'receiver')

# Register your models here.
admin.site.register(Message, MessageAdmin)