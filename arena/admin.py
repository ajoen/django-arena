from django.contrib import admin
from .models import Forum, ForumCategory


class ForumAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ForumCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Forum, ForumAdmin)
admin.site.register(ForumCategory, ForumCategoryAdmin)