from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_contactos, name='lista_contactos'),
    path('nuevo/', views.crear_contacto, name='crear_contacto'),
    path('contacto/<int:contacto_id>/', views.detalle_contacto, name='detalle_contacto'),
    path('borrar/<int:contacto_id>/', views.borrar_contacto, name='borrar_contacto'),
]