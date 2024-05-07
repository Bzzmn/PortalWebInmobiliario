import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inmobiliario.settings')
django.setup()


from webPages.models import Inmueble, Comuna 

def fetch_inmuebles():

    comunas = Comuna.objects.prefetch_related('inmuebles').all()
    inmuebles_por_comuna = {}
    
    for comuna in comunas:
        inmuebles = comuna.inmuebles.filter(disponible=True).values('nombre', 'descripcion')
        if inmuebles:
            inmuebles_por_comuna[comuna.nombre] = list(inmuebles)
    
    return inmuebles_por_comuna

def save_to_file(data, filename='inmuebles_por_comuna.txt'):
    with open(filename, 'w', encoding="utf-8") as file:
        for comuna, inmuebles in data.items():
            file.write(f"Comuna: {comuna}\n")
            for inmueble in inmuebles:
                file.write(f"  Nombre: {inmueble['nombre']}\n")
                file.write(f"  Descripción: {inmueble['descripcion']}\n")
            file.write("\n")

if __name__ == '__main__':
    inmuebles_data = fetch_inmuebles()
    save_to_file(inmuebles_data)