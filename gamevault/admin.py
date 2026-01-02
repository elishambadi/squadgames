

# admin.py
from django.contrib import admin
from .models import Game, Category, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty', 'min_players', 'max_players', 'views', 'created_at']
    list_filter = ['difficulty', 'categories', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['categories']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'game', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'author__username', 'game__title']
    readonly_fields = ['created_at']
    