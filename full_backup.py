import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inmobiliario.settings')
django.setup()

from django.core.serializers import serialize
import json

def backup_data():
    from webPages.models import Usuario, Arrendador, Arrendatario, Datos, Inmueble, Comuna, TipoDeInmueble, Solicitud, Region

    output_data = []

    regiones = serialize('json', Region.objects.all(), use_natural_foreign_keys=True)

    comunas = serialize('json', Comuna.objects.all(), use_natural_foreign_keys=True)
    tipos_de_inmueble = serialize('json', TipoDeInmueble.objects.all(), use_natural_foreign_keys=True)

    usuarios = serialize('json', Usuario.objects.all())
    arrendadores = serialize('json', Arrendador.objects.all())
    arrendatarios = serialize('json', Arrendatario.objects.all())

    datos_usuarios = serialize('json', Datos.objects.all())

    inmuebles = serialize('json', Inmueble.objects.all())

    solicitudes = serialize('json', Solicitud.objects.all())

    output_data.extend(json.loads(regiones))
    output_data.extend(json.loads(comunas))
    output_data.extend(json.loads(tipos_de_inmueble))
    output_data.extend(json.loads(usuarios))
    output_data.extend(json.loads(arrendadores))
    output_data.extend(json.loads(arrendatarios))
    output_data.extend(json.loads(datos_usuarios))
    output_data.extend(json.loads(inmuebles))
    output_data.extend(json.loads(solicitudes))

    with open('full_backup.json', 'w', encoding="utf-8") as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    import django
    django.setup()
    backup_data()