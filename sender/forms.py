from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from sender.models import MassSend, Client, ClientGroup


class RequestKwargModelFormMixin(object):
    """Миксин для выхвата реквеста внутри формы
    (форма должна находиться во вьюшке с миксином RequestFormKwargsMixin)
    """
    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop(
            "request", None
        )
        super(RequestKwargModelFormMixin, self).__init__(*args, **kwargs)


class MassSendForm(RequestKwargModelFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Изменение виджетов в форме для соответствующих полей
        self.fields['start_date'].widget = AdminDateWidget(attrs={'type': 'date'})
        self.fields['periodicity'].widget = forms.RadioSelect(choices=[('1', 'Каждый день'), ('7', 'Каждую неделю'), ('30', 'Каждый месяц')])
        self.fields['group'] = forms.ModelChoiceField(queryset=ClientGroup.objects.filter(owner=self.request.user))

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


