from django.urls import path

from sender.views import HomepageView, MassSendCreateView, MassSendDetailView, ClientCreateView, \
    ClientUpdateView, ClientDetailView, ClientDeleteView, ClientListView, MassSendListView, MassSendUpdateView, \
    MassSendDeleteView, ClientGroupEdit, ClientGroupListView, ClientGroupCreateView, ClientGroupDetailView, \
    ClientGroupUpdateView, ClientGroupDeleteView, add_client, remove_client, MassendManagerView, block_send, \
    ManagerUsersView, ManagerMassendsView

app_name = 'sender'


urlpatterns = [
    path('', HomepageView.as_view(), name='home'),
    # Рассылки
    path('massends', MassSendListView.as_view(), name="massend_list"),
    path('massends/create', MassSendCreateView.as_view(), name='massend_create'),
    path('massends/massend/<int:pk>/update', MassSendUpdateView.as_view(), name='massend_update'),
    path('massends/massend/<int:pk>/', MassSendDetailView.as_view(), name='massend_detail'),
    path('massends/massend/<int:pk>/delete', MassSendDeleteView.as_view(), name='massend_delete'),
    # Клиенты
    path('clients', ClientListView.as_view(), name='client_list'),
    path('clients/create', ClientCreateView.as_view(), name='client_create'),
    path('clients/client/<int:pk>/update', ClientUpdateView.as_view(), name='client_update'),
    path('clients/client/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('clients/client/<int:pk>/delete', ClientDeleteView.as_view(), name='client_delete'),
    # Группы
    path('groups', ClientGroupListView.as_view(), name='group_list'),
    path('groups/create', ClientGroupCreateView.as_view(), name='group_create'),
    path('groups/group/<int:pk>', ClientGroupDetailView.as_view(), name='group_detail'),
    path('groups/group/<int:pk>/update', ClientGroupUpdateView.as_view(), name='group_update'),
    path('groups/group/<int:pk>/delete', ClientGroupDeleteView.as_view(), name='group_delete'),
    path('groups/group/<int:pk>/edit', ClientGroupEdit.as_view(), name='group_edit'),
    path('add_client/<int:group_id>/<int:client_id>', add_client, name='add_client'),
    path('remove_client/<int:group_id>/<int:client_id>', remove_client, name='remove_client'),

    # Менеджер
    path('manager/massend/<int:pk>', MassendManagerView.as_view(), name='massend_manager'),
    path('manager/massends', ManagerMassendsView.as_view(), name='massends_manager'),
    path('manager/massend/<int:pk>/ban', block_send, name='ban_send'),
    path('manager/users', ManagerUsersView.as_view(), name='users_manager'),
]

