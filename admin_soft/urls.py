from django.urls import path
from admin_soft import views
from django.contrib.auth import views as auth_views

from .views import (see_qr,submit_review,simple_review,
                    visitor_statistics,export_visitor_statistics_csv,
                    thank_you_view,dashboard,manual_entry,add_department,add_purpose,
                    delete_purpose,delete_department
                    )


urlpatterns = [
    path('', views.see_qr, name='qr'),    
    path('pages/submit-review/', submit_review, name='submit-review'),
    path('pages/simple-review/<str:phone_number>/', simple_review, name='simple-review'),
    path('thankyou/', views.thank_you_view, name='thankyou'),  
    path('thanks/', views.thanks, name='thanks'),  
    path('pages/dashboard/', views.dashboard, name='dashboard'),  
    path('pages/manual/', views.manual_entry, name='manual_entry'),  



    path('pages/visitor_statistics', visitor_statistics, name='visitor_statistics'),
    path('visitor_statistics/csv/', export_visitor_statistics_csv, name='export_visitor_statistics_csv'),


    # Authentication
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    # path('accounts/register/', views.register, name='register'),
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


        path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path ('add_user', views.add_user, name='add_user'),



    path('pages/add_department/', views.add_department, name='add_department'),
    path('pages/edit_department/<int:id>/', views.edit_department, name='edit_department'),
    path('pages/delete_department/<int:id>/', views.delete_department, name='delete_department'),

    path('pages/add_purpose/', views.add_purpose, name='add_purpose'),
    path('pages/edit_purpose/<int:id>/', views.edit_purpose, name='edit_purpose'),
    path('pages/delete_purpose/<int:id>/', views.delete_purpose, name='delete_purpose'),
]
