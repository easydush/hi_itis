from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from base.models import Group


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ('title', 'course')