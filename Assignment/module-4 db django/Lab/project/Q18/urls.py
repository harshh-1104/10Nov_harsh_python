from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='q18_signup'),
    path('verify-otp/', views.verify_otp_view, name='q18_verify_otp'),
    path('login/', views.login_view, name='q18_login'),
    path('logout/', views.logout_view, name='q18_logout'),

    path('', views.dashboard_view, name='q18_dashboard'),
    path('transactions/', views.transaction_list_view, name='q18_transactions'),
    path('categories/', views.category_list_view, name='q18_categories'),
    path('budgets/', views.budget_list_view, name='q18_budgets'),
    path('reports/', views.reports_view, name='q18_reports'),
    path('profile/', views.profile_view, name='q18_profile'),
    path('transactions/delete/<int:pk>/', views.delete_transaction_view, name='q18_delete_transaction'),
    path('categories/delete/<int:pk>/', views.delete_category_view, name='q18_delete_category'),
    path('budgets/delete/<int:pk>/', views.delete_budget_view, name='q18_delete_budget'),
    path('emi/', views.emi_list_view, name='q18_emi'),
    path('emi/delete/<int:pk>/', views.delete_emi_view, name='q18_delete_emi'),
]
