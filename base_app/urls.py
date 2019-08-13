from django.urls import path

from . import views

app_name = "base_app"

urlpatterns = [
    path('address/', views.AddressView.as_view(), name='address'),
]