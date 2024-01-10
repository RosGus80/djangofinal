from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from sender.models import MassSend, Client, ClientGroup


class MassSendForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].widget = AdminDateWidget(attrs={'type': 'date'})

    class Meta:
        model = MassSend
        exclude = ('owner', 'end_date', 'banned')


class MassendManagerForm(forms.ModelForm):
    class Meta:
        model = MassSend
        fields = ('banned',)


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('owner', )


class ClientGroupForm(forms.ModelForm):
    class Meta:
        model = ClientGroup
        fields = ('name', )


