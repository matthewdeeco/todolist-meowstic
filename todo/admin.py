from django.contrib import admin
from todo.models import *

class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ("created_on",)

admin.site.register(Item, ItemAdmin)