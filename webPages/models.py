from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class CustomUserManager(UserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Crea y guarda un usuario con el email dado y la contraseña.
        """
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class Usuario(AbstractUser):

    username = None
    email = models.EmailField('email', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    es_arrendador = models.BooleanField(default=False)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    rut = models.CharField(max_length=9, primary_key=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="usuario_set",
        related_query_name="usuario",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="usuario_set",
        related_query_name="usuario",
    )

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

class Arrendador(Usuario):
    pass  

class Arrendatario(Usuario):
    pass  

class Datos(models.Model):
    direccion = models.CharField(max_length=100, default='')
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='datos')

class Inmueble(models.Model):
    nombre = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='inmuebles')
    direccion = models.CharField(max_length=100)
    comuna = models.ForeignKey('Comuna', on_delete=models.SET_NULL, related_name='inmuebles', null=True)
    descripcion = models.TextField()
    superficie_construida = models.FloatField()
    superficie_total = models.FloatField()
    cantidad_estacionamientos = models.IntegerField(default=1)
    cantidad_habitaciones = models.IntegerField(default=1)
    cantidad_banos = models.IntegerField(default=1)
    tipo_de_inmueble = models.ForeignKey('TipoDeInmueble', on_delete=models.SET_NULL, related_name='inmuebles', null=True)
    precio_arriendo = models.IntegerField()
    disponible = models.BooleanField(default=True)
    fecha_publicacion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)
    arrendador = models.ForeignKey('Arrendador', on_delete=models.CASCADE, related_name='inmuebles')

class Solicitud(models.Model):

    class EstadoSolicitud(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        ACEPTADA = 'aceptada', 'Aceptada'
        RECHAZADA = 'rechazada', 'Rechazada'

    inmueble = models.ForeignKey('Inmueble', on_delete=models.CASCADE, related_name='solicitudes')
    arrendatario = models.ForeignKey('Arrendatario', on_delete=models.CASCADE, related_name='solicitudes')
    estado = models.CharField(
        max_length=10,
        choices=EstadoSolicitud.choices,
        default=EstadoSolicitud.PENDIENTE,
    )
    mensaje = models.TextField(default='Hola, me gusta su propiedad, me gustaría arrendarla.')
    fecha_solicitud = models.DateField(auto_now_add=True)
    fecha_aceptacion = models.DateField(null=True)
    fecha_rechazo = models.DateField(null=True)

class Region(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre,)  

class Comuna(models.Model):
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey('Region', on_delete=models.CASCADE, related_name='comunas')
    
    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre,) 

    class Meta:
        unique_together = (('nombre', 'region'),)

class TipoDeInmueble(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def natural_key(self):
        return (self.nombre,)  

    def __str__(self):
        return self.nombre





