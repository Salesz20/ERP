from django.urls import path
from . import views

urlpatterns = [
    path('', views.crm_home, name='crm_home'),
    path('companies/', views.company_list, name='company_list'),
    path('contacts/', views.contact_list, name='contact_list'),
    path('opportunities/', views.opportunity_list, name='opportunity_list'),
    path('tasks/', views.task_list, name='task_list'),
]
