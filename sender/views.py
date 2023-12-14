from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView
from datetime import timedelta

from sender.forms import MassSendForm, ClientForm, ClientGroupForm
from sender.models import MassSend, ClientGroup, Client


# Create your views here.


def send_email(context):
    send_mail(
        "Subject here",
        "Here is the message.",
        'noreply@gmail.com',
        ["rosgus80@gmail.com"],
        fail_silently=False,
    )
    return redirect(reverse_lazy('sender:home'))


class HomepageView(TemplateView):
    template_name = 'sender/base.html'


# Вьюшки для рассылок
class MassSendCreateView(LoginRequiredMixin, CreateView):
    model = MassSend
    form_class = MassSendForm
    template_name = 'sender/send/create.html'
    success_url = reverse_lazy('sender:home')

    def form_valid(self, form):
        """Если форма валидна, задать значения для владельца, равное текущему пользователю,
        а конечную дату - начальной дате + 2 дня"""
        new_obj = form.save(commit=False)
        new_obj.owner = self.request.user
        new_obj.end_date = new_obj.start_date + timedelta(days=1)
        new_obj.save()
        if new_obj.start_date <= datetime.today().date() <= new_obj.end_date:
            print('success')
        return super().form_valid(form)


class MassSendUpdateView(LoginRequiredMixin, UpdateView):
    model = MassSend
    form_class = MassSendForm
    template_name = 'sender/send/create.html'
    success_url = reverse_lazy('sender:home')

    def form_valid(self, form):
        """То же самое, что для создания, но без задачи нового значения пользователю в силу ненужности"""
        new_obj = form.save(commit=False)
        new_obj.end_date = new_obj.start_date + timedelta(days=1)
        new_obj.save()
        if new_obj.start_date <= datetime.today().date() <= new_obj.end_date:
            print('success')
        return super().form_valid(form)


class MassSendDetailView(LoginRequiredMixin, DetailView):
    model = MassSend
    template_name = 'sender/send/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = self.object.group
        return context


class MassSendDeleteView(DeleteView):
    model = MassSend
    template_name = 'sender/send/delete.html'
    success_url = reverse_lazy('sender:massend_list')


class MassSendListView(LoginRequiredMixin, TemplateView):
    template_name = 'sender/send/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sends'] = MassSend.objects.filter(owner=self.request.user)
        return context


# Вьюшки для клиентов
class ClientCreateView(CreateView):
    model = Client
    template_name = 'sender/client/create.html'
    form_class = ClientForm
    success_url = reverse_lazy('sender:client_list')

    def form_valid(self, form):
        new_obj = form.save(commit=False)
        new_obj.owner = self.request.user
        new_obj.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'sender/client/create.html'
    form_class = ClientForm
    success_url = reverse_lazy('sender:client_list')


class ClientDetailView(DetailView):
    model = Client
    template_name = 'sender/client/detail.html'


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'sender/client/delete.html'
    success_url = reverse_lazy('sender:client_list')


class ClientListView(LoginRequiredMixin, TemplateView):
    template_name = 'sender/client/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = Client.objects.filter(owner=self.request.user)
        return context


# Вьюшки для групп
class ClientGroupCreateView(CreateView):
    model = ClientGroup
    template_name = 'sender/group/create.html'
    form_class = ClientGroupForm
    success_url = reverse_lazy('sender:group_list')

    def form_valid(self, form):
        new_obj = form.save(commit=False)
        new_obj.owner = self.request.user
        new_obj.save()
        return super().form_valid(form)


class ClientGroupUpdateView(UpdateView):
    model = ClientGroup
    template_name = 'sender/group/create.html'
    form_class = ClientGroupForm
    success_url = reverse_lazy('sender:group_list')


class ClientGroupDetailView(DetailView):
    model = ClientGroup
    template_name = 'sender/group/detail.html'


class ClientGroupDeleteView(DeleteView):
    model = ClientGroup
    template_name = 'sender/group/delete.html'
    success_url = reverse_lazy('sender:group_list')


class ClientGroupListView(LoginRequiredMixin, TemplateView):
    template_name = 'sender/group/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = ClientGroup.objects.filter(owner=self.request.user)
        return context


class ClientGroupEdit(LoginRequiredMixin, DetailView):
    model = ClientGroup
    template_name = 'sender/group/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients_included'] = self.get_object().clients.all()
        # Создаю список из всех групп пользователя и исключаю из них те,
        # которые находятся в кверисете context['clients_included']
        context['clients_not_included'] = Client.objects.filter(owner=self.request.user).exclude(id__in=context['clients_included'])
        return context


# Сервисные вьюшки
def add_client(request, group_id, client_id):
    """Функция для добавления клиента в выбранную группу из шаблона edit без видимой смены страницы"""
    client = Client.objects.get(pk=client_id)
    group = ClientGroup.objects.get(pk=group_id)
    group.clients.add(client)
    return redirect(reverse_lazy('sender:group_edit', kwargs={'pk': group_id}))


def remove_client(request, group_id, client_id):
    """Функция для удаления клиента из выбранной группы из шаблона edit без видимой смены страницы"""
    client = Client.objects.get(pk=client_id)
    group = ClientGroup.objects.get(pk=group_id)
    group.clients.remove(client)
    return redirect(reverse_lazy('sender:group_edit', kwargs={'pk': group_id}))

