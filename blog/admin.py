from django.contrib import admin

# Register your models here.
from .models import Post, Tag, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'user']
    fields = ['title', 'body', 'category', 'tags',  'excerpt']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)