from django.urls import path
from admin_soft import views
from django.contrib.auth import views as auth_views

from .views import (see_qr,submit_review,simple_review,
                    visitor_statistics,export_visitor_statistics_csv,
                    thank_you_view,dashboard,manual_entry)


urlpatterns = [
    # path('index/', views.index, name='index'),
    path('', views.see_qr, name='qr'),    #changed
    path('pages/submit-review/', submit_review, name='submit-review'),
    path('pages/simple-review/<str:phone_number>/', simple_review, name='simple-review'),
    path('thankyou/', views.thank_you_view, name='thankyou'),  
    path('pages/dashboard/', views.dashboard, name='dashboard'),  
    path('pages/manual/', views.manual_entry, name='manual_entry'),  



    path('pages/visitor_statistics', visitor_statistics, name='visitor_statistics'),
    path('visitor_statistics/csv/', export_visitor_statistics_csv, name='export_visitor_statistics_csv'),
    # Authentication
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name="password_change_done"),
    path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', 
        views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
   
# ]

