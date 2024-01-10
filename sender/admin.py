from django.contrib import admin

from sender.models import MassSend, ClientGroup, Client, Log


@admin.register(ClientGroup)
class ClientGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name')


@admin.register(MassSend)
class MassSendAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('date', 'is_sent', 'server_response')
