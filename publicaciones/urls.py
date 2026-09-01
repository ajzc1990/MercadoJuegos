from django.urls import path
from . import views

app_name = 'publicaciones'

urlpatterns = [
    path('<int:pk>/', views.detalle_producto, name='detalle'),
    path('crear/', views.crear_producto, name='crear'),
    path('responder/<int:pregunta_id>/', views.responder_pregunta, name='responder'),
]