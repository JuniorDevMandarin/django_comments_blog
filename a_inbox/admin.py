from django.contrib import admin

# Register your models here.
import django.db
from .models import *

class InboxMessageAdmin(admin.ModelAdmin):
    readonly_fields = ('sender', 'conversation', 'body')

admin.site.register(InboxMessage, InboxMessageAdmin)
admin.site.register(Conversation)
