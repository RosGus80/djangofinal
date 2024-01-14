import random

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView
from datetime import timedelta

from blog.models import Post
from sender.forms import MassSendForm, ClientForm, ClientGroupForm, MassendManagerForm
from sender.models import MassSend, ClientGroup, Client
from users.models import User


# Create your views here.


class HomepageView(TemplateView):
    template_name = 'sender/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_manager'] = True if self.request.user.groups.filter(name='Manager').exists() else False
            context['user_massends_num'] = MassSend.objects.filter(owner=self.request.user).count()
            context['user_active_massends_num'] = MassSend.objects.filter(owner=self.request.user, is_active=True).count()
            context['unique_clients_num'] = Client.objects.filter(owner=self.request.user).distinct().count()

        posts = list(Post.objects.all())
        if len(posts) >= 3:
            context['random_posts'] = random.sample(posts, 3)
        else:
            context['random_posts'] = random.sample(posts, len(posts))

        return context


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


class MassSendUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MassSend
    form_class = MassSendForm
    template_name = 'sender/send/update.html'
    success_url = reverse_lazy('sender:home')

    def test_func(self):
        if self.object.owner == self.request.user:
            return True
        else:
            return False

    def form_valid(self, form):
        """То же самое, что для создания, но без задачи нового значения пользователю в силу ненужности"""
        new_obj = form.save(commit=False)
        new_obj.end_date = new_obj.start_date + timedelta(days=1)
        new_obj.save()
        if new_obj.start_date <= datetime.today().date() <= new_obj.end_date:
            print('success')
        return super().form_valid(form)


class MassSendDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = MassSend
    template_name = 'sender/send/detail.html'

    def test_func(self):
        if self.get_object().owner == self.request.user or self.request.user.groups.filter(name='Manager').exists():
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = self.object.group
        return context


class MassSendDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MassSend
    template_name = 'sender/send/delete.html'
    success_url = reverse_lazy('sender:massend_list')

    def test_func(self):
        if self.get_object().owner == self.request.user:
            return True
        else:
            return False


class MassSendListView(LoginRequiredMixin, TemplateView):
    template_name = 'sender/send/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sends'] = MassSend.objects.filter(owner=self.request.user)
        return context


# Вьюшки для клиентов
class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    template_name = 'sender/client/create.html'
    form_class = ClientForm
    success_url = reverse_lazy('sender:client_list')

    def form_valid(self, form):
        new_obj = form.save(commit=False)
        new_obj.owner = self.request.user
        new_obj.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    template_name = 'sender/client/update.html'
    form_class = ClientForm
    success_url = reverse_lazy('sender:client_list')

    def test_func(self):
        if self.get_object().owner == self.request.user:
            return True
        else:
            return False


class ClientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Client
    template_name = 'sender/client/detail.html'

    def test_func(self):
        if self.get_object().owner == self.request.user:
            return True
        else:
            return False


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    template_name = 'sender/client/delete.html'
    success_url = reverse_lazy('sender:client_list')

    def test_func(self):
        if self.get_object().owner == self.request.user:
            return True
        else:
            return False


class ClientListView(LoginRequiredMixin, TemplateView):
    template_name = 'sender/client/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = Client.objects.filter(owner=self.request.user)
        return context


# Вьюшки для групп
class ClientGroupCreateView(LoginRequiredMixin, CreateView):
    model = ClientGroup
    template_name = 'sender/group/create.html'
    form_class = ClientGroupForm
    success_url = reverse_lazy('sender:group_list')

    def form_valid(self, form):
        new_obj = form.save(commit=False)
        new_obj.owner = self.request.user
        new_obj.save()
        return super().form_valid(form)


class ClientGroupUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ClientGroup
    template_name = 'sender/group/update.html'
    form_class = ClientGroupForm
    success_url = reverse_lazy('sender:group_list')

    def test_func(self):
        if self.get_object().owner == self.request.user:
            return True
        else:
            return False


class ClientGroupDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ClientGroup
    template_name = 'sender/group/detail.html'

    def test_func(self):
        if self.get_object().owner == self.request.user:
            return True
        else:
            return False


class ClientGroupDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ClientGroup
    template_name = 'sender/group/delete.html'
    success_url = reverse_lazy('sender:group_list')

    def test_func(self):
        if self.get_object().owner == self.request.user:
            return True
        else:
            return False


class ClientGroupListView(LoginRequiredMixin, TemplateView):
    template_name = 'sender/group/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = ClientGroup.objects.filter(owner=self.request.user)
        return context


class ClientGroupEdit(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ClientGroup
    template_name = 'sender/group/edit.html'

    def test_func(self):
        if self.get_object().owner == self.request.user:
            return True
        else:
            return False

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
    # user_passes_test(client.owner == request.user and group.owner == request.user)
    group.clients.add(client)
    return redirect(reverse_lazy('sender:group_edit', kwargs={'pk': group_id}))


def remove_client(request, group_id, client_id):
    """Функция для удаления клиента из выбранной группы из шаблона edit без видимой смены страницы"""
    client = Client.objects.get(pk=client_id)
    group = ClientGroup.objects.get(pk=group_id)
    # user_passes_test(client.owner == request.user and group.owner == request.user)
    group.clients.remove(client)
    return redirect(reverse_lazy('sender:group_edit', kwargs={'pk': group_id}))

# Менеджер


class MassendManagerView(UpdateView, UserPassesTestMixin):
    model = MassSend
    form_class = MassendManagerForm
    template_name = 'sender/manager/massend_update.html'
    success_url = reverse_lazy('sender:massends_manager')

    def test_func(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return True
        else:
            return False


def block_send(request, pk):
    if request.user.groups.filter(name='Manager').exists():
        send = MassSend.objects.get(pk=pk)
        send.banned = True
        send.save()
    return redirect(reverse_lazy('sender:manager'))


class ManagerUsersView(UserPassesTestMixin, TemplateView):
    template_name = 'sender/manager/users.html'

    def test_func(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = True if self.request.user.groups.filter(name='Manager').exists() else False
        context['users'] = User.objects.all()
        return context


class ManagerMassendsView(UserPassesTestMixin, TemplateView):
    template_name = 'sender/manager/massends.html'

    def test_func(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = True if self.request.user.groups.filter(name='Manager').exists() else False
        context['massends'] = MassSend.objects.all()
        return context