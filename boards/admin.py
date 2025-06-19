from django.contrib import admin
from boards.models import Board, Topic, Post

admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post)

class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_deleted')
    list_filter = ('is_deleted',)