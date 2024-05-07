import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inmobiliario.settings')
django.setup()

from django.core.serializers import serialize
import json

def backup_inmuebles():
    from webPages.models import Inmueble, Comuna, TipoDeInmueble

    output_data = []

    comunas = serialize('json', Comuna.objects.all(), use_natural_foreign_keys=True)
    tipos_de_inmueble = serialize('json', TipoDeInmueble.objects.all(), use_natural_foreign_keys=True)

    inmuebles = serialize('json', Inmueble.objects.all(), use_natural_foreign_keys=True)

    output_data.extend(json.loads(comunas))
    output_data.extend(json.loads(tipos_de_inmueble))
    output_data.extend(json.loads(inmuebles))

    with open('backup_inmuebles.json', 'w', encoding="utf-8") as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    import django
    django.setup()
    backup_inmuebles()