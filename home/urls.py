from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('contacto/', views.contacto, name='contacto'),
]