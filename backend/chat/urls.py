from django.urls import path
from . import views
from .views import FrontendAppView

urlpatterns = [
    path('channels/create/', views.create_channel, name='create_channel'),
    path('channels/<int:pk>/join/', views.join_channel, name='join_channel'),
    path('channels/<int:pk>/leave/', views.leave_channel, name='leave_channel'),
    path('channels/my/', views.my_channels, name='my_channels'),
    path('messages/<int:channel_id>/', views.list_messages, name='list_messages'),
    path('channels/<int:channel_id>/messages/', views.send_message, name='send_message'),
    path("channels/", views.list_channels, name="list_channels"),
    path("channels/<int:channel_id>/", views.channel_name, name="channel_name"),

    path("test/", views.test_socket_view, name="test_socket"),
    # path('', index, name='home'),
    path("test/react/", FrontendAppView.as_view(), name="frontend")
]
