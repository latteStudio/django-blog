from django.contrib import admin
from .models import Comments

# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_time']
    fields = ['name', 'email', 'text', 'website']


admin.site.register(Comments, CommentAdmin)
