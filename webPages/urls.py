from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("registro/arrendador/", views.registroArrendador, name="registroArrendador"),
    path(
        "registro/arrendatario/",
        views.registroArrendatario,
        name="registroArrendatario",
    ),
    path("registro/datos/", views.registroDatos, name="registroDatos"),
    path("login/", views.customLogin, name="login"),
    path("panel/arrendador/", views.panelArrendador, name="panelArrendador"),
    path("panel/arrendatario/", views.panelArrendatario, name="panelArrendatario"),
    path(
        "registro/inmueble/",
        views.InmuebleCreateView.as_view(),
        name="registroInmueble",
    ),
    path("update/inmueble/", views.InmuebleUpdateView.as_view(), name="updateInmueble"),
    path(
        "solicitud/arriendo/<int:inmueble_id>/",
        views.solicitarArriendo,
        name="solicitarArriendo",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("registro/seleccion", views.seleccionarUsuario, name="seleccionarUsuario"),
    path("inmueble/<int:inmueble_id>/", views.detalleInmueble, name="detalleInmueble"),
    path("redirigir_panel/", views.redirigirPanel, name="redirigirPanel"),
    path(
        "cancelar_solicitud/<int:solicitud_id>/",
        views.cancelarSolicitud,
        name="cancelarSolicitud",
    ),
    path(
        "eliminar_solicitud/<int:solicitud_id>/",
        views.eliminarSolicitud,
        name="eliminarSolicitud",
    ),
    path(
        "aceptar_solicitud/<int:solicitud_id>/",
        views.aceptarSolicitud,
        name="aceptarSolicitud",
    ),
    path(
        "rechazar_solicitud/<int:solicitud_id>/",
        views.rechazarSolicitud,
        name="rechazarSolicitud",
    ),
    path(
        "ocultar_inmueble/<int:inmueble_id>/",
        views.ocultarInmueble,
        name="ocultarInmueble",
    ),
    path(
        "eliminar_inmueble/<int:inmueble_id>/",
        views.eliminarInmueble,
        name="eliminarInmueble",
    ),
    path(
        "mostrar_inmueble/<int:inmueble_id>/",
        views.mostrarInmueble,
        name="mostrarInmueble",
    ),
    path("get_comunas/", views.get_comunas, name="get_comunas"),
]
