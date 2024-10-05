from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Correo electrónico", unique=True, help_text="Dirección de correo electrónico del usuario")
    nombre = models.CharField("Nombre", max_length=50, help_text="Nombre del usuario")
    apellido = models.CharField("Apellido", max_length=50, help_text="Apellido del usuario")
    rut = models.CharField("RUT", max_length=9, primary_key=True, help_text="RUT del usuario (formato: 12345678-9)")
    es_arrendador = models.BooleanField("Es arrendador", default=False, help_text="Indica si el usuario es un arrendador")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['nombre', 'apellido', 'rut']

    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="grupos",
        blank=True,
        help_text="Los grupos a los que pertenece este usuario. Un usuario obtendrá todos los permisos otorgados a cada uno de sus grupos.",
        related_name="usuario_set",
        related_query_name="usuario",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="permisos de usuario",
        blank=True,
        help_text="Permisos específicos para este usuario.",
        related_name="usuario_set",
        related_query_name="usuario",
    )

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"


class ArrendadorManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(es_arrendador=True)

    def get_by_natural_key(self, email):
        return self.get(**{self.model.USERNAME_FIELD: email})
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('es_arrendador', True)
        return super().create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('es_arrendador', True)
        return super().create_superuser(email, password, **extra_fields)


class Arrendador(Usuario):
    objects = ArrendadorManager()

    def natural_key(self):
        return (self.email,)

    class Meta:
        proxy = True
        verbose_name = "arrendador"
        verbose_name_plural = "arrendadores"


class Arrendatario(Usuario):
    class Meta:
        proxy = True
        verbose_name = "arrendatario"
        verbose_name_plural = "arrendatarios"


class Datos(models.Model):
    direccion = models.CharField("Dirección", max_length=100, default="", help_text="Dirección del usuario")
    telefono = models.CharField("Teléfono", max_length=15, help_text="Número de teléfono del usuario")
    email = models.EmailField("Correo electrónico", help_text="Correo electrónico de contacto")
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="datos", verbose_name="Usuario",
        help_text="Usuario asociado a estos datos"
    )

    class Meta:
        verbose_name = "datos de usuario"
        verbose_name_plural = "datos de usuarios"


class Solicitud(models.Model):

    class EstadoSolicitud(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        ACEPTADA = "aceptada", "Aceptada"
        RECHAZADA = "rechazada", "Rechazada"

    inmueble = models.ForeignKey(
        "Inmueble", on_delete=models.CASCADE, related_name="solicitudes",
        verbose_name="Inmueble", help_text="Inmueble asociado a esta solicitud"
    )
    arrendatario = models.ForeignKey(
        "Arrendatario", on_delete=models.CASCADE, related_name="solicitudes",
        verbose_name="Arrendatario", help_text="Arrendatario que realiza la solicitud"
    )
    estado = models.CharField(
        "Estado", max_length=10, choices=EstadoSolicitud.choices,
        default=EstadoSolicitud.PENDIENTE, help_text="Estado actual de la solicitud"
    )
    mensaje = models.TextField(
        "Mensaje", default="Hola, me gusta su propiedad, me gustaría arrendarla.",
        help_text="Mensaje del arrendatario al arrendador"
    )
    fecha_solicitud = models.DateField("Fecha de solicitud", auto_now_add=True, help_text="Fecha en que se realizó la solicitud")
    fecha_aceptacion = models.DateField("Fecha de aceptación", null=True, help_text="Fecha en que se aceptó la solicitud")
    fecha_rechazo = models.DateField("Fecha de rechazo", null=True, help_text="Fecha en que se rechazó la solicitud")

    class Meta:
        verbose_name = "solicitud"
        verbose_name_plural = "solicitudes"


class Region(models.Model):
    nombre = models.CharField("Nombre", max_length=100, unique=True, help_text="Nombre de la región")

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre,)

    def get_comunas(self):
        return self.comunas.all()

    class Meta:
        verbose_name = "región"
        verbose_name_plural = "regiones"


class ComunaManager(models.Manager):
    def get_by_natural_key(self, nombre, region_nombre):
        return self.get(nombre=nombre, region__nombre=region_nombre)


class Comuna(models.Model):
    nombre = models.CharField("Nombre", max_length=100, help_text="Nombre de la comuna")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="comunas", verbose_name="Región", help_text="Región a la que pertenece la comuna")
    objects = ComunaManager()

    def __str__(self):
        return f"{self.nombre} ({self.region.nombre})"

    def natural_key(self):
        return (self.nombre, self.region.nombre)

    class Meta:
        unique_together = (("nombre", "region"),)
        constraints = [
            models.UniqueConstraint(
                fields=["nombre", "region"], name="unique_nombre_region"
            )
        ]
        verbose_name = "comuna"
        verbose_name_plural = "comunas"


class TipoDeInmuebleManager(models.Manager):
    def get_by_natural_key(self, nombre):
        return self.get(nombre=nombre)


class TipoDeInmueble(models.Model):
    nombre = models.CharField("Nombre", max_length=100, unique=True, help_text="Nombre del tipo de inmueble")
    objects = TipoDeInmuebleManager()

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre,)

    class Meta:
        verbose_name = "tipo de inmueble"
        verbose_name_plural = "tipos de inmueble"


class Inmueble(models.Model):
    nombre = models.CharField("Nombre", max_length=50, help_text="Nombre o título del inmueble")
    imagen_url = models.URLField(
        "URL de la imagen",
        max_length=1000,
        default="https://via.placeholder.com/300x200.png?text=No+Image",
        help_text="URL de la imagen principal del inmueble en S3"
    )
    direccion = models.CharField("Dirección", max_length=100, help_text="Dirección del inmueble")
    comuna = models.ForeignKey(
        Comuna, on_delete=models.SET_NULL, related_name="inmuebles", null=True,
        verbose_name="Comuna", help_text="Comuna donde se ubica el inmueble"
    )
    descripcion = models.TextField("Descripción", help_text="Descripción detallada del inmueble")
    superficie_construida = models.FloatField("Superficie construida", help_text="Superficie construida en metros cuadrados")
    superficie_total = models.FloatField("Superficie total", help_text="Superficie total del terreno en metros cuadrados")
    cantidad_estacionamientos = models.IntegerField("Cantidad de estacionamientos", default=1, help_text="Número de estacionamientos disponibles")
    cantidad_habitaciones = models.IntegerField("Cantidad de habitaciones", default=1, help_text="Número de habitaciones")
    cantidad_banos = models.IntegerField("Cantidad de baños", default=1, help_text="Número de baños")
    tipo_de_inmueble = models.ForeignKey(
        TipoDeInmueble, to_field="nombre", on_delete=models.SET_NULL, related_name="inmuebles", null=True,
        verbose_name="Tipo de inmueble", help_text="Tipo de inmueble (casa, departamento, etc.)"
    )
    precio_arriendo = models.IntegerField("Precio de arriendo", help_text="Precio mensual de arriendo")
    disponible = models.BooleanField("Disponible", default=True, help_text="Indica si el inmueble está disponible para arrendar")
    fecha_publicacion = models.DateField("Fecha de publicación", auto_now_add=True, help_text="Fecha en que se publicó el inmueble")
    fecha_actualizacion = models.DateField("Fecha de actualización", auto_now=True, help_text="Fecha de la última actualización")
    arrendador = models.ForeignKey(
        Usuario, to_field="email", on_delete=models.CASCADE, related_name="inmuebles",
        limit_choices_to={"es_arrendador": True}, verbose_name="Arrendador",
        help_text="Usuario arrendador que publica el inmueble"
    )

    def __str__(self):
        return f"{self.nombre} en {self.comuna}"

    class Meta:
        verbose_name = "inmueble"
        verbose_name_plural = "inmuebles"