
from django.urls import path, include
from zoho import views

urlpatterns = [
    path('zoho', views.zoho)
]