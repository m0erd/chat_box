from django.urls import path
from . import views

urlpatterns = [
    path('channels/create/', views.create_channel, name='create_channel'),
    path('channels/<int:pk>/join/', views.join_channel, name='join_channel'),
    path('channels/<int:pk>/leave/', views.leave_channel, name='leave_channel'),
    path('channels/my/', views.my_channels, name='my_channels'),
]


# from django.urls import include, path
# from rest_framework.routers import DefaultRouter
# # from .views import ChannelViewSet
#
# from . import views
#
# urlpatterns = [
#     path('channels/', views.channel_list_create, name='channel-list-create'),
#     path('channels/<int:pk>/', views.channel_detail, name='channel-detail'),
#     path('channels/<int:pk>/join/', views.join_channel, name='join-channel'),
#     path('channels/<int:pk>/leave/', views.leave_channel, name='leave-channel'),
#     path('my-channels/', views.my_channels, name='my-channels'),
# ]
#
# # router = DefaultRouter()
# # router.register(r'channels', ChannelViewSet)
# #
# # urlpatterns = [
# #     path('api/', include(router.urls)),
# # ]
