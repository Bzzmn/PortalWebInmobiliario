# Documentación de Modelos y Funcionalidades CRUD

## Modelos

### Usuario
- Base para los usuarios, extendiendo `AbstractUser`.
- Campos personalizados incluyen `email`, `nombre`, `apellido`, `rut`, y `es_arrendador`.
- Maneja autenticación basada en el correo electrónico en lugar del nombre de usuario tradicional.

### Arrendador y Arrendatario
- Subclases del modelo `Usuario` para diferenciar entre roles de usuario.

### Datos
- Almacena información de contacto de usuarios incluyendo dirección, teléfono y email.
- Relación uno-a-uno con `Usuario`.

### Inmueble
- Representa propiedades disponibles para arrendar.
- Incluye detalles como tipo de inmueble, dirección, descripción, superficie, y más.
- Relacionado con `Arrendador` a través de una clave foránea.

### Solicitud
- Gestiona las solicitudes de arriendo de inmuebles.
- Estado puede ser pendiente, aceptado o rechazado.
- Relacionado con `Inmueble` y `Arrendatario`.

## CRUD - Crear, Leer, Actualizar, Eliminar

### Inmuebles
- **Crear Inmuebles**: Los arrendadores pueden registrar inmuebles nuevos.
- **Ver Inmuebles**: Todos los usuarios pueden ver detalles de inmuebles disponibles.
- **Actualizar Inmuebles**: Los arrendadores pueden modificar detalles de sus inmuebles.
- **Eliminar Inmuebles**: Funcionalidad para que los arrendadores eliminen inmuebles.

### Usuarios
- **Registro de Arrendadores y Arrendatarios**: Se pueden registrar como arrendadores o arrendatarios.
- **Login y Autenticación**: Autenticación basada en correo electrónico y contraseña.
- **Actualizar Datos de Contacto**: Usuarios pueden actualizar su información de contacto.

### Solicitudes de Arriendo
- **Crear Solicitudes de Arriendo**: Arrendatarios pueden solicitar el arriendo de inmuebles.
- **Ver Estado de Solicitudes**: Usuarios pueden ver el estado de sus solicitudes.
- **Cancelar o Modificar Solicitudes**: Arrendatarios pueden cancelar o modificar solicitudes pendientes.

## Validaciones y Mejoras de Experiencia de Usuario

- **Validación de Rol**: Solo arrendatarios pueden hacer solicitudes de arriendo; arrendadores están restringidos de esta acción.
- **Propiedad Propia**: Usuarios no pueden solicitar arriendo de inmuebles que ellos mismos han registrado.
- **Datos de Contacto**: Se requiere que los usuarios tengan datos de contacto registrados antes de poder realizar o aceptar solicitudes de arriendo.
- **Solicitudes Duplicadas**: Se previene que los usuarios hagan múltiples solicitudes para el mismo inmueble.

Estas validaciones aseguran que la plataforma funcione de manera justa y eficiente, y mejora la experiencia general del usuario al prevenir errores comunes y comportamiento no deseado.