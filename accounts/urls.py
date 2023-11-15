from django.urls import path
from . import views

urlpatterns = [
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('user/profile/', views.profile, name="profile"),
    path('user/reading-list/', views.reading_list, name="reading-list"),
    path('user/continue-reading', views.continue_reading, name='continue-reading'),
    path('user/notifications', views.notifications, name='notifications'),
    path('ajax/auth/login', views.login, name='login'),
    path('auth/login', views.logout, name='logout'),
    path('ajax/auth/register', views.register, name='register'),
    path('ajax/user/profile', views.change_avatar, name="change-avatar"),
    path('ajax/auth/forgot', views.forgot, name='forgot'),
    path('password-reset-confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password-reset-confirm'),
    path('ajax/reading-list/add', views.add_reading_list, name='add-reading-list'),
    path('ajax/user/log-reading', views.log_reading, name='log-reading'),
    path('ajax/continue-reading/remove', views.remove_continue_reading, name='remove-continue-reading'),
    path('ajax/continue-reading/home', views.continue_reading_home, name="continue-reading-home"),
    path('ajax/notification/seen-all', views.notification_seen_all, name="notification_seen_all"),
]
