from django.contrib import admin

# Register your models here.

from xss.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
