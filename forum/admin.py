from django.contrib import admin

from .models import ForumPost, ForumReply

admin.site.register(ForumPost)
admin.site.register(ForumReply)
