from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect


from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import ArrendatarioRegisterForm, ArrendadorRegisterForm, DatosForm, CustomLoginForm, InmuebleForm, SolicitudForm
from .models import Inmueble, Arrendador, Arrendatario, Solicitud, Datos
# Create your views here.

#HOMEPAGE
def home(request):
    inmuebles = Inmueble.objects.filter(disponible=True)
    return render(request, 'pages/home.html', {'inmuebles': inmuebles})

# REGISTRO DE USUARIOS -ARRENDADOR
def registroArrendador(request):
    if request.method == 'POST':
        form = ArrendadorRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=form.cleaned_data.get('email'), password=password)
            if user:
                login(request, user)
                return redirect('panelArrendador')
    else:
        form = ArrendadorRegisterForm()
    return render(request, 'pages/registroUsuario.html', {'form': form})

# REGISTRO DE USUARIOS -ARRENDATARIO
def registroArrendatario(request):
    if request.method == 'POST':
        form = ArrendatarioRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=form.cleaned_data.get('email'), password=password)
            if user:
                login(request, user)
                return redirect('panelArrendatario')
    else:
        form = ArrendatarioRegisterForm()
    return render(request, 'pages/registroUsuario.html', {'form': form})

# LOGIN
def customLogin(request):
    if request.method == 'POST':
        form = CustomLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if user.is_staff:
                return redirect('admin:index')

            elif user.es_arrendador:
                return redirect('panelArrendador')

            else:
                return redirect('panelArrendatario')
  
    else:
        form = CustomLoginForm(request=request)
    return render(request, 'pages/login.html', {'form': form})


# PANEL DE USUARIO - ARRENDADOR
@login_required
def panelArrendador(request):

    try:
        datos_instance = Datos.objects.get(usuario=request.user)
    except Datos.DoesNotExist:
        datos_instance = None

    if request.method == 'POST':
        form = DatosForm(request.POST, user=request.user,  instance=datos_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos registrados correctamente')
            return redirect('panelArrendador')

    elif not request.user.is_authenticated or not request.user.es_arrendador:
        return redirect('login')

    else:   
        form = DatosForm(instance=datos_instance, user=request.user)
        inmuebles = Inmueble.objects.filter(arrendador=request.user)  
        solicitudes_pendientes = Solicitud.objects.filter(inmueble__in=inmuebles, estado='pendiente')
        solicitudes_aceptadas = Solicitud.objects.filter(inmueble__in=inmuebles, estado='aceptada')
        solicitudes_rechazadas = Solicitud.objects.filter(inmueble__in=inmuebles, estado='rechazada')
        
        context = {
            'inmuebles': inmuebles,
            'solicitudes_pendientes': solicitudes_pendientes,
            'solicitudes_aceptadas': solicitudes_aceptadas,
            'solicitudes_rechazadas': solicitudes_rechazadas,
            'form': form,
        }

        return render(request, 'pages/panelArrendador.html' , context)

# PANEL DE USUARIO - ARRENDATARIO
@login_required
def panelArrendatario(request):
    try:
        datos_instance = Datos.objects.get(usuario=request.user)
    except Datos.DoesNotExist:
        datos_instance = None

    if request.method == 'POST':
        form = DatosForm(request.POST, user=request.user,  instance=datos_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos registrados correctamente')
            return redirect('panelArrendador')

    elif not request.user.is_authenticated or request.user.es_arrendador:
        return redirect('login')

    else:

        form = DatosForm(instance=datos_instance, user=request.user)
        solicitudes = Solicitud.objects.filter(arrendatario=request.user)

        context = {
            'solicitudes': solicitudes,
            'form': form
        }

        return render(request, 'pages/panelArrendatario.html', context )

#REGISTRO DE DATOS DE CONTACTO
@login_required
def registroDatos(request):
    if request.method == 'POST':
        form = DatosForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'pages/registroDatos.html', {'form': form})
    else:
        form = DatosForm(user=request.user)
        return render(request, 'pages/registroDatos.html', {'form': form})


# REGISTRO DE INMUEBLES ARRENDADOR 
class ArrendadorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.es_arrendador


# CREAR INMUEBLE
class InmuebleCreateView(LoginRequiredMixin, ArrendadorRequiredMixin, CreateView):
    model = Inmueble
    form_class = InmuebleForm
    template_name = 'pages/inmuebleForm.html'
    success_url = reverse_lazy('panelArrendador')


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.es_arrendador:
            return redirect('login')
        if not Datos.objects.filter(usuario=request.user).exists():
            messages.error(request, 'Debes registrar tus datos de contacto antes de publicar un inmueble')
            return redirect('panelArrendador')
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = self.request.user

        try:
            arrendador = Arrendador.objects.get(rut=user.rut)
            print('arrendador:', arrendador, 'user:', user, 'rut:', user.rut)
            kwargs.update({'user': arrendador})
        except Arrendador.DoesNotExist:
            kwargs.update({'user': None})
            print('se actualizó el diccionario con user: None')
        return kwargs

#ACTUALIZAR INMUEBLE < pendiente de revisión >
class InmuebleUpdateView(LoginRequiredMixin, ArrendadorRequiredMixin, UpdateView):
    model = Inmueble
    form_class = InmuebleForm
    template_name = 'pages/inmuebleForm.html'
    success_url = reverse_lazy('panelArrendador')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = self.request.user

        try:
            arrendador = Arrendador.objects.get(rut=user.rut)
            kwargs.update({'user': arrendador})
        except Arrendador.DoesNotExist:
            kwargs.update({'user': None})
        return kwargs

# ELIMINAR INMUEBLE < pendiente de revisión >

# SOLICITAR ARRIENDO
@login_required
def solicitarArriendo(request, inmueble_id):

    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    usuario = request.user

    if usuario.es_arrendador:
        messages.error(request, 'Solo los arrendatarios pueden realizar solicitudes de arriendo.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    elif inmueble.arrendador == usuario:
        messages.error(request, 'No puedes realizar una solicitud para tu propio inmueble.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    elif not Datos.objects.filter(usuario=request.user).exists():
        messages.error(request, 'Debes ingresar tus datos de contacto antes de realizar una solicitud.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    elif Solicitud.objects.filter(inmueble=inmueble).exists():
        messages.error(request, 'Ya has enviado una solicitud para este inmueble.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


    else:
        try:
            arrendatario = Arrendatario.objects.get(pk=usuario.pk)

        except Arrendatario.DoesNotExist:
            messages.error(request, 'Debes registrarte como arrendatario antes de realizar una solicitud.')
            return redirect('registroArrendatario')

        if request.method == 'POST':
            form = SolicitudForm(request.POST, inmueble=inmueble, arrendatario=arrendatario)
            if form.is_valid():
                form.save()
                messages.success(request, 'Solicitud de arriendo creada correctamente.')
                return redirect('panelArrendatario')

        else:
            form = SolicitudForm(inmueble=inmueble, arrendatario=arrendatario)
            return render(request, 'pages/solicitudArriendo.html', {'form': form, 'inmueble': inmueble})




