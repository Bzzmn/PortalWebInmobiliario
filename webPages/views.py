from django.views.generic.edit import CreateView, UpdateView
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django import template

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import (
    ArrendatarioRegisterForm,
    ArrendadorRegisterForm,
    DatosForm,
    CustomLoginForm,
    InmuebleForm,
    SolicitudForm,
    PropertySearchForm,
)
from .models import (
    Inmueble,
    Arrendador,
    Arrendatario,
    Solicitud,
    Datos,
    Region,
)
from .utils import upload_to_s3

register = template.Library()

# Create your views here.


# HOMEPAGE
def home(request):
    form = PropertySearchForm(request.GET or None)
    inmuebles = Inmueble.objects.filter(disponible=True)

    if form.is_valid():
        if form.cleaned_data["tipo_de_inmueble"]:
            inmuebles = inmuebles.filter(
                tipo_de_inmueble=form.cleaned_data["tipo_de_inmueble"]
            )
        if form.cleaned_data["comuna"]:
            inmuebles = inmuebles.filter(comuna=form.cleaned_data["comuna"])
        elif form.cleaned_data["region"]:
            inmuebles = inmuebles.filter(comuna__region=form.cleaned_data["region"])

    context = {
        "form": form,
        "inmuebles": inmuebles,
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "components/inmuebles_list.html", context)
    return render(request, "pages/home.html", context)


def get_comunas(request):
    region_id = request.GET.get("region_id")
    comunas = []
    if region_id:
        region = Region.objects.get(id=region_id)
        comunas = list(region.comunas.order_by("nombre").values("id", "nombre"))
    return JsonResponse({"comunas": comunas})


# REGISTRO DE USUARIOS -ARRENDADOR
def registroArrendador(request):
    if request.method == "POST":
        form = ArrendadorRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            password = form.cleaned_data.get("password1")
            user = authenticate(
                request, username=form.cleaned_data.get("email"), password=password
            )
            if user:
                login(request, user)
                messages.success(request, "Registro exitoso. Bienvenido!")
                return redirect("panelArrendador")
            else:
                messages.error(request, "No se pudo iniciar sesión automáticamente. Por favor, inicie sesión.")
        else:
            messages.error(request, "Por favor, corrija los errores en el formulario.")
    else:
        form = ArrendadorRegisterForm()
    return render(request, "pages/registroUsuario.html", {"form": form})


# REGISTRO DE USUARIOS -ARRENDATARIO
def registroArrendatario(request):
    if request.method == "POST":
        form = ArrendatarioRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            password = form.cleaned_data.get("password1")
            user = authenticate(
                request, username=form.cleaned_data.get("email"), password=password
            )
            if user:
                login(request, user)
                return redirect("panelArrendatario")
    else:
        form = ArrendatarioRegisterForm()
    return render(request, "pages/registroUsuario.html", {"form": form})


# LOGIN
def customLogin(request):
    if request.method == "POST":
        form = CustomLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenido, {user.nombre}!")
            if user.is_staff:
                return redirect("admin:index")
            elif user.es_arrendador:
                return redirect("panelArrendador")
            else:
                return redirect("panelArrendatario")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = CustomLoginForm(request=request)
    return render(request, "pages/login.html", {"form": form})


# PANEL DE USUARIO - ARRENDADOR
@login_required
def panelArrendador(request):

    try:
        datos_instance = Datos.objects.get(usuario=request.user)
    except Datos.DoesNotExist:
        datos_instance = None

    if request.method == "POST":
        form = DatosForm(request.POST, user=request.user, instance=datos_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos registrados correctamente")
            return redirect("panelArrendador")

    elif not request.user.is_authenticated or not request.user.es_arrendador:
        return redirect("login")

    else:
        form = DatosForm(instance=datos_instance, user=request.user)
        inmuebles = Inmueble.objects.filter(arrendador=request.user)
        solicitudes = Solicitud.objects.filter(inmueble__in=inmuebles).exclude(
            estado="rechazada"
        )

        context = {
            "inmuebles": inmuebles,
            "solicitudes": solicitudes,
            "form": form,
            "datos": datos_instance,
        }

        return render(request, "pages/panelArrendador.html", context)


# PANEL DE USUARIO - ARRENDATARIO
@login_required
def panelArrendatario(request):
    if not request.user.is_authenticated or request.user.es_arrendador:
        return redirect("login")

    try:
        datos_instance = Datos.objects.get(usuario=request.user)
    except Datos.DoesNotExist:
        datos_instance = None

    if request.method == "POST":
        form = DatosForm(request.POST, user=request.user, instance=datos_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos registrados correctamente")
            return redirect("panelArrendatario")

    else:
        user = get_object_or_404(Arrendatario, pk=request.user.pk)
        form = DatosForm(instance=datos_instance, user=request.user)
        solicitudes = Solicitud.objects.filter(arrendatario=request.user)

        context = {
            "solicitudes": solicitudes,
            "form": form,
            "user": user,
            "datos": datos_instance,
        }

        return render(request, "pages/panelArrendatario.html", context)


# REGISTRO DE DATOS DE CONTACTO
@login_required
def registroDatos(request):
    if request.method == "POST":
        form = DatosForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            return render(request, "pages/registroDatos.html", {"form": form})
    else:
        form = DatosForm(user=request.user)
        return render(request, "pages/registroDatos.html", {"form": form})


# REGISTRO DE INMUEBLES ARRENDADOR
class ArrendadorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.es_arrendador


# CREAR INMUEBLE
class InmuebleCreateView(LoginRequiredMixin, ArrendadorRequiredMixin, CreateView):
    model = Inmueble
    form_class = InmuebleForm
    template_name = "pages/inmuebleForm.html"
    success_url = reverse_lazy("panelArrendador")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.es_arrendador:
            return redirect("login")
        if not Datos.objects.filter(usuario=request.user).exists():
            messages.error(
                request,
                "Debes registrar tus datos de contacto antes de publicar un inmueble",
            )
            return redirect("panelArrendador")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = self.request.user

        try:
            arrendador = Arrendador.objects.get(rut=user.rut)
            print("arrendador:", arrendador, "user:", user, "rut:", user.rut)
            kwargs.update({"user": arrendador})
        except Arrendador.DoesNotExist:
            kwargs.update({"user": None})
            print("se actualizó el diccionario con user: None")
        return kwargs

    def form_valid(self, form):
        inmueble = form.save(commit=False)
        inmueble.arrendador = self.request.user

        imagen = self.request.FILES.get('imagen')
        if imagen:
            imagen_url = upload_to_s3(imagen)
            inmueble.imagen_url = imagen_url

        inmueble.save()
        messages.success(self.request, "Inmueble creado exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Por favor, corrija los errores en el formulario.")
        return super().form_invalid(form)


# ACTUALIZAR INMUEBLE < pendiente de revisión >
class InmuebleUpdateView(LoginRequiredMixin, ArrendadorRequiredMixin, UpdateView):
    model = Inmueble
    form_class = InmuebleForm
    template_name = "pages/inmuebleForm.html"
    success_url = reverse_lazy("panelArrendador")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = self.request.user

        try:
            arrendador = Arrendador.objects.get(rut=user.rut)
            kwargs.update({"user": arrendador})
        except Arrendador.DoesNotExist:
            kwargs.update({"user": None})
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Inmueble actualizado exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Por favor, corrija los errores en el formulario.")
        return super().form_invalid(form)


# ELIMINAR INMUEBLE < pendiente de revisión >


# SOLICITAR ARRIENDO
@login_required
def solicitarArriendo(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    usuario = request.user

    if usuario.es_arrendador:
        messages.error(
            request, "Solo los arrendatarios pueden realizar solicitudes de arriendo."
        )
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

    if inmueble.arrendador == usuario:
        messages.error(
            request, "No puedes realizar una solicitud para tu propio inmueble."
        )
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

    if not Datos.objects.filter(usuario=request.user).exists():
        messages.error(
            request,
            "Debes ingresar tus datos de contacto antes de realizar una solicitud.",
        )
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

    if Solicitud.objects.filter(inmueble=inmueble, arrendatario=usuario).exists():
        messages.error(request, "Ya has enviado una solicitud para este inmueble.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

    try:
        arrendatario = Arrendatario.objects.get(pk=usuario.pk)
    except Arrendatario.DoesNotExist:
        messages.error(
            request,
            "Debes registrarte como arrendatario antes de realizar una solicitud.",
        )
        return redirect("registroArrendatario")

    if request.method == "POST":
        form = SolicitudForm(request.POST, inmueble=inmueble, arrendatario=arrendatario)
        if form.is_valid():
            form.save()
            messages.success(request, "Solicitud de arriendo creada correctamente.")
            return redirect("panelArrendatario")
    else:
        form = SolicitudForm(inmueble=inmueble, arrendatario=arrendatario)

    return render(
        request, "pages/solicitudArriendo.html", {"form": form, "inmueble": inmueble}
    )


# SELECCION TIPO DE USUARIO
def seleccionarUsuario(request):
    return render(request, "pages/registro_seleccion.html")


# DETALLE DE INMUEBLE
def detalleInmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    return render(request, "pages/detalleInmueble.html", {"inmueble": inmueble})


# REDIRIGIR A PANEL DE USUARIO
@login_required
def redirigirPanel(request):
    if request.user.es_arrendador:
        return redirect("panelArrendador")
    else:
        return redirect("panelArrendatario")


# ELIMINAR SOLICITUD
@login_required
@require_http_methods(["POST"])
def eliminarSolicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id, arrendatario=request.user)
    solicitud.delete()
    return JsonResponse({"success": True}, status=200)


# CANCELAR SOLICITUD
@login_required
@require_http_methods(["POST"])
def cancelarSolicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id, arrendatario=request.user)
    solicitud.delete()
    return JsonResponse({"success": True}, status=200)


# ACEPTAR SOLICITUD
@login_required
@require_http_methods(["POST"])
def aceptarSolicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    solicitud.estado = "aceptada"
    solicitud.inmueble.disponible = False
    solicitud.save()
    return JsonResponse({"success": True}, status=200)


# RECHAZAR SOLICITUD
@login_required
@require_http_methods(["POST"])
def rechazarSolicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    solicitud.estado = "rechazada"
    solicitud.save()
    return JsonResponse({"success": True}, status=200)


# OCULTAR INMUEBLE
@login_required
@require_http_methods(["POST"])
def ocultarInmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id, arrendador=request.user)
    inmueble.disponible = False
    inmueble.save()
    return JsonResponse({"success": True}, status=200)


# MOSTRAR INMUEBLE
@login_required
@require_http_methods(["POST"])
def mostrarInmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id, arrendador=request.user)
    inmueble.disponible = True
    inmueble.save()
    return JsonResponse({"success": True}, status=200)


# ELIMINAR INMUEBLE
@login_required
@require_http_methods(["POST"])
def eliminarInmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id, arrendador=request.user)
    inmueble.delete()
    messages.success(request, "Inmueble eliminado exitosamente.")
    return JsonResponse({"success": True}, status=200)


