from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/arrendador/', views.registroArrendador, name='registroArrendador'),
    path('registro/arrendatario/', views.registroArrendatario, name='registroArrendatario'),
    path('registro/datos/', views.registroDatos, name='registroDatos'),
    path('login/', views.customLogin, name='login'),
    path('panel/arrendador/', views.panelArrendador, name='panelArrendador'),
    path('panel/arrendatario/', views.panelArrendatario, name='panelArrendatario'),
    path('registro/inmueble/', views.InmuebleCreateView.as_view(), name='registroInmueble'),
    path('update/inmueble/', views.InmuebleUpdateView.as_view(), name='updateInmueble'),
    path('solicitud/arriendo/<int:inmueble_id>/', views.solicitarArriendo, name='solicitarArriendo'),
]

