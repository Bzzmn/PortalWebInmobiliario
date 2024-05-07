import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inmobiliario.settings')
django.setup()

import json
from django.contrib.auth.hashers import make_password

usuarios = [
    {'email': 'arrendador1@mail.com', 'nombre': 'Jose', 'apellido': 'Lopez', 'rut': '123456781', 'direccion': 'Calle B 461', 'telefono': '964887228', 'es_arrendador': True},
    {'email': 'arrendador2@mail.com', 'nombre': 'Luis', 'apellido': 'Fuenzalida', 'rut': '123456782', 'direccion': 'Calle E 426', 'telefono': '951636146', 'es_arrendador': True},
    {'email': 'arrendador3@mail.com', 'nombre': 'Fernando', 'apellido': 'Carrasco', 'rut': '123456783', 'direccion': 'Calle C 765', 'telefono': '951453566', 'es_arrendador': True},
    {'email': 'arrendador4@mail.com', 'nombre': 'Jorge', 'apellido': 'Gerjo', 'rut': '122342678', 'direccion': 'Calle A 345', 'telefono': '983758875', 'es_arrendador': True},
    {'email': 'arrendador5@mail.com', 'nombre': 'Francisco', 'apellido': 'Olivares', 'rut': '147686783', 'direccion': 'Calle F 907', 'telefono': '951509446', 'es_arrendador': True},
    {'email': 'arrendador6@mail.com', 'nombre': 'Patricia', 'apellido': 'Fernandez', 'rut': '123458873', 'direccion': 'Calle G 74573', 'telefono': '977553566', 'es_arrendador': True},
    {'email': 'arrendador7@mail.com', 'nombre': 'Carolina', 'apellido': 'Perez', 'rut': '123457683', 'direccion': 'Calle H 636', 'telefono': '951994566', 'es_arrendador': True},
    {'email': 'arrendador8@mail.com', 'nombre': 'Constanza', 'apellido': 'Navarro', 'rut': '123444783', 'direccion': 'Calle I 7134', 'telefono': '952298566', 'es_arrendador': True},
    {'email': 'arrendador9@mail.com', 'nombre': 'Lorena', 'apellido': 'Diaz', 'rut': '123988778', 'direccion': 'Calle J 945', 'telefono': '951945666', 'es_arrendador': True},
    {'email': 'arrendatario1@mail.com', 'nombre': 'Karin', 'apellido': 'Manriquez', 'rut': '166540965', 'direccion': 'Calle D 834', 'telefono': '950892373', 'es_arrendador': False},
    {'email': 'arrendatario2@mail.com', 'nombre': 'Ana', 'apellido': 'Garcia', 'rut': '166545252', 'direccion': 'Calle K 923', 'telefono': '988348073', 'es_arrendador': False},
]

def generate_fixtures(usuarios, output_file):
    all_data = []
    for usuario in usuarios:
        # Agregar usuario general
        all_data.append({
            "model": "webPages.usuario",
            "pk": usuario['rut'],
            "fields": {
                "email": usuario['email'],
                "password": make_password('password123'),
                "nombre": usuario['nombre'],
                "apellido": usuario['apellido'],
                "rut": usuario['rut'],
                "es_arrendador": usuario['es_arrendador']
            }
        })
        # Agregar específicamente arrendador o arrendatario
        user_model = "webPages.arrendador" if usuario['es_arrendador'] else "webPages.arrendatario"
        all_data.append({
            "model": user_model,
            "pk": usuario['rut'],
            "fields": {
                "usuario_ptr_id": usuario['rut']
            }
        })
        # Agregar datos
        all_data.append({
            "model": "webPages.datos",
            "fields": {
                "direccion": usuario['direccion'],
                "telefono": usuario['telefono'],
                "email": usuario['email'],
                "usuario": usuario['rut']
            }
        })

    with open(output_file, 'w', encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)

# Generar el archivo JSON
generate_fixtures(usuarios, 'usuarios_datos.json')
print("Archivo JSON generado exitosamente.")