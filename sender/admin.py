from django.contrib import admin

from sender.models import MassSend, ClientGroup, Client


@admin.register(ClientGroup)
class ClientGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name')

@admin.register(MassSend)
class MassSendAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')