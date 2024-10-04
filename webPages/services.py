from .models import Datos, Inmueble, Solicitud
from django.contrib.auth import get_user_model
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import IntegrityError

User = get_user_model()

def create_arrendador(email, password, nombre, apellido, rut, direccion, telefono):
    try:
        if User.objects.filter(email=email).exists():
            raise ValidationError("El email ya está en uso.")
        if User.objects.filter(rut=rut).exists():
            raise ValidationError("El RUT ya está registrado.")

        arrendador = User.objects.create_user(
            email=email, password=password, nombre=nombre, apellido=apellido, rut=rut
        )
        arrendador.es_arrendador = True
        arrendador.save()

        Datos.objects.create(
            usuario=arrendador,
            direccion=direccion,
            telefono=telefono,
            email=email
        )

        return arrendador
    except IntegrityError as e:
        raise ValidationError(f"Error al crear el arrendador: {str(e)}") from e

def create_arrendatario(email, password, nombre, apellido, rut, direccion, telefono):
    try:
        if User.objects.filter(email=email).exists():
            raise ValidationError("El email ya está en uso.")
        if User.objects.filter(rut=rut).exists():
            raise ValidationError("El RUT ya está registrado.")

        arrendatario = User.objects.create_user(
            email=email, password=password, nombre=nombre, apellido=apellido, rut=rut
        )
        arrendatario.es_arrendador = False
        arrendatario.save()

        Datos.objects.create(
            usuario=arrendatario,
            direccion=direccion,
            telefono=telefono,
            email=email
        )

        return arrendatario
    except IntegrityError as e:
        raise ValidationError(f"Error al crear el arrendatario: {str(e)}") from e

def create_inmueble(
    nombre,
    imagen,
    direccion,
    comuna,
    region,
    descripcion,
    superficie_construida,
    superficie_total,
    cantidad_estacionamientos,
    cantidad_habitaciones,
    cantidad_banos,
    tipo_de_inmueble,
    precio_arriendo,
    disponible,
    arrendador,
):
    try:
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
            arrendador=arrendador,
        )
        return inmueble
    except IntegrityError as e:
        raise ValidationError(f"Error al crear el inmueble: {str(e)}") from e

def update_inmueble(disponible, inmueble):
    try:
        inmueble.disponible = disponible
        inmueble.save()
    except Exception as e:
        raise ValidationError(f"Error al actualizar el inmueble: {str(e)}") from e

def delete_inmueble(inmueble):
    try:
        inmueble.delete()
    except Exception as e:
        raise ValidationError(f"Error al eliminar el inmueble: {str(e)}") from e

def create_solicitud(arrendatario, inmueble, fecha_inicio, fecha_termino, mensaje):
    try:
        solicitud = Solicitud.objects.create(
            arrendatario=arrendatario,
            inmueble=inmueble,
            fecha_inicio=fecha_inicio,
            fecha_termino=fecha_termino,
            mensaje=mensaje,
        )
        return solicitud
    except IntegrityError as e:
        raise ValidationError(f"Error al crear la solicitud: {str(e)}") from e

def aceptar_solicitud(solicitud):
    try:
        solicitud.estado = Solicitud.EstadoSolicitud.ACEPTADA
        solicitud.fecha_aceptacion = datetime.now()
        solicitud.save()
    except Exception as e:
        raise ValidationError(f"Error al aceptar la solicitud: {str(e)}") from e

def rechazar_solicitud(solicitud):
    try:
        solicitud.estado = Solicitud.EstadoSolicitud.RECHAZADA
        solicitud.fecha_rechazo = datetime.now()
        solicitud.save()
    except Exception as e:
        raise ValidationError(f"Error al rechazar la solicitud: {str(e)}") from e
