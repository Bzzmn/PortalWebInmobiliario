import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inmobiliario.settings')
django.setup()

from webPages.models import Inmueble, Comuna, Region

def fetch_inmuebles_por_region():

    regiones_con_inmuebles = Region.objects.prefetch_related(
        'comunas__inmuebles'
    ).filter(comunas__inmuebles__disponible=True).distinct()

    inmuebles_por_region = {}

    for region in regiones_con_inmuebles:
        inmuebles_list = []
        for comuna in region.comunas.all():
            inmuebles = comuna.inmuebles.filter(disponible=True).values('nombre', 'descripcion')
            inmuebles_list.extend(list(inmuebles))
        if inmuebles_list:
            inmuebles_por_region[region.nombre] = inmuebles_list

    return inmuebles_por_region


def save_to_file(inmuebles_data, filename='inmuebles_por_region.txt'):
    with open(filename, 'w', encoding='utf-8') as file:
        for region, inmuebles in inmuebles_data.items():
            file.write(f"Región: {region}\n")
            for inmueble in inmuebles:
                file.write(f"  Nombre: {inmueble['nombre']}\n")
                file.write(f"  Descripción: {inmueble['descripcion']}\n")
            file.write("\n")

if __name__ == '__main__':
    inmuebles_data = fetch_inmuebles_por_region()
    save_to_file(inmuebles_data)