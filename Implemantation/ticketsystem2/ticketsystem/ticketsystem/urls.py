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
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetView, PasswordResetConfirmView, \
    PasswordResetCompleteView
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
    path('account/add-event', views.add_event, name='add_event'),
    path('account/reset-password/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('admin/operator/add', views.add_operator, name='operator_add'),
    path('admin/operator/all', views.operators_list_view, name='operator_all'),
    path('admin/user/all', views.users_list_view, name='users_all'),
    path('balance/add/', views.add_balance, name='add_balance'),
    path('admin/event/waiting/', views.waiting_events, name='waiting_events'),
    path('admin/event/active/', views.accepted_events, name='active_events'),
    path('admin/event/reject/', views.rejected_events, name='rejected_events'),
    path('admin/event/disactive/', views.disactive_events, name='disactive_events'),
    path('admin/event/approve/<int:event_id>', views.approve_event, name='approve_event'),
    path('admin/event/reject/<int:event_id>', views.reject_event, name='reject_event'),
    path('admin/stage/all/', views.stage_list_view, name='stage_all'),
    path('admin/stage/add/',views.add_stage_view,name='stage_add'),
    path('admin/stage/edit/',views.edit_stage_view,name='stage_edit'),
    path('event/search-event/', views.search_event, name='search_event'),
    path('admin/stage/<int:stage_id>/edit', views.edit_stage_view, name='stage_edit'),
    path('admin/stage/<int:stage_id>/delete', views.delete_stage_view, name='stage_delete'),
    path('event/theatre/', views.theatre_events, name='theatre_event'),
    path('event/concert/', views.concert_events, name='concert_event'),
    path('event/sport/', views.sport_events, name='sport_event'),
    path('event/<int:event_id>/edit', views.edit_event, name='edit_event'),
    path('event/<int:event_id>/delete', views.delete_event, name='delete_event'),
    path('event/<int:event_id>/check', views.event_check, name='check_event'),
    path('search/results' , views.search_with_opinions, name='opinion_search'),
    path('my-events/', views.my_events, name='my_events'),
    path('my-transactions/', views.collect_tickets, name='my_transactions'),
    path('transaction/<int:transaction_id>', views.my_tickets_view, name='transaction'),
    path('event/search-all/', views.overall_search, name='overall_search'),
]
