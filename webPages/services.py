from .models import Arrendador, Arrendatario, Datos, Inmueble, Solicitud
from django.contrib.auth import get_user_model


def create_arrendador(username, password, nombre, apellido, rut, direccion, telefono, email):
    
    Arrendador = get_user_model()
    arrendador = Arrendador.objects.create_user(
        username=username, 
        password=password, 
        nombre=nombre, 
        apellido=apellido, 
        rut=rut)
    arrendador.es_arrendador = True
    arrendador.save()
    
    datos = Datos.objects.create(
        direccion=direccion, 
        telefono=telefono, 
        email=email, 
        usuario=arrendador)
    
    return arrendador


def create_arrendatario(username, password, nombre, apellido, rut, direccion, telefono, email):
    
    Arrendatario = get_user_model() 
    arrendatario = Arrendatario.objects.create_user(
        username=username, 
        password=password, 
        nombre=nombre, 
        apellido=apellido, 
        rut=rut)
    arrendatario.es_arrendador = False
    arrendatario.save()
    
    datos = Datos.objects.create(
        direccion=direccion, 
        telefono=telefono, 
        email=email, 
        usuario=arrendatario)
    
    return arrendatario


def create_inmueble(nombre, imagen, direccion, comuna, region, descripcion, superficie_construida, superficie_total, cantidad_estacionamientos, cantidad_habitaciones, cantidad_banos, tipo_de_inmueble, precio_arriendo, disponible, arrendador):
    
    inmueble = Inmueble.objects.create(
        nombre=nombre, 
        imagen=imagen, 
        direccion=direccion, 
        comuna=comuna, 
        region=region, 
        descripcion=descripcion, 
        superficie_construida=superficie_construida, 
        superficie_total=superficie_total, 
        cantidad_estacionamientos=cantidad_estacionamientos, 
        cantidad_habitaciones=cantidad_habitaciones, 
        cantidad_banos=cantidad_banos, 
        tipo_de_inmueble=tipo_de_inmueble,
        precio_arriendo=precio_arriendo,
        disponible=disponible,
        arrendador=arrendador)
    return inmueble

def update_inmueble(disponible, inmueble):
    inmueble.disponible = disponible
    inmueble.save()

def delete_inmueble(inmueble):
    inmueble.delete()

def create_solicitud(arrendatario, inmueble, fecha_inicio, fecha_termino, mensaje):
    
    solicitud = Solicitud.objects.create(
        arrendatario=arrendatario, 
        inmueble=inmueble, 
        fecha_inicio=fecha_inicio, 
        fecha_termino=fecha_termino, 
        mensaje=mensaje)
    
    return solicitud

def aceptar_solicitud(solicitud):
    solicitud.aceptada = True
    solicitud.fecha_aceptacion = datetime.now()
    solicitud.save()

def rechazar_solicitud(solicitud):
    solicitud.aceptada = False
    solicitud.fecha_rechazo = datetime.now()
    solicitud.save()
