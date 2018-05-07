
from django.urls import path, include
from zoho import views

urlpatterns = [
    path('update', views.update_chart_mogul)
]