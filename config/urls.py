from django.urls import include, path

urlpatterns = [
    path('apps/zoho/', include('zoho.urls'))
]
