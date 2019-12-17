"""ticketsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from website import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('admin/', admin.site.urls),
    path('event/<int:pk>/preview', views.event_preview, name='event_preview'),
    path('event/<int:pk>/buy', views.ticket_buy_view, name='buy_ticket'),
    path('account/tickets/', views.my_tickets_view, name='my_tickets'),
    path('account/tickets/<int:pk>/preview', views.ticket_preview, name='ticket_preview'),
    path('account/profile/', views.my_profile_view, name='my_profile'),
    path('account/profile/edit', views.edit_my_profile, name='edit_my_profile'),
    path('account/change-password/', views.change_password, name='change_password'),
    path('account/reset-password/', PasswordResetView.as_view(), name='password_reset'),
    path('account/reset-password/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('account/reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('account/reset-password/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete')
]
