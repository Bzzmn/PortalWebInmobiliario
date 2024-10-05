from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import (
    Arrendador,
    Arrendatario,
    Datos,
    Inmueble,
    Solicitud,
    Comuna,
    Region,
    TipoDeInmueble,
)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field


# FORM DE REGISTRO DE USUARIO ARRENDADOR
class ArrendadorRegisterForm(UserCreationForm):
    class Meta:
        model = Arrendador
        fields = ["email", "nombre", "apellido", "rut", "password1", "password2"]
        widgets = {"password": forms.PasswordInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(
            Submit("submit", "Completar registro", css_class="btn btn-primary")
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.es_arrendador = True
        user.set_password(self.cleaned_data["password1"])
        user.username = user.email.lower()
        user.is_staff = False
        if commit:
            user.save()
        return user


# FORM DE REGISTRO DE USUARIO ARRENDATARIO
class ArrendatarioRegisterForm(UserCreationForm):
    class Meta:
        model = Arrendatario
        fields = ["email", "nombre", "apellido", "rut", "password1", "password2"]
        widgets = {"password": forms.PasswordInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(
            Submit("submit", "Completar registro", css_class="btn btn-primary")
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.es_arrendador = False
        user.set_password(self.cleaned_data["password1"])
        user.username = user.email.lower()
        user.is_staff = False
        if commit:
            user.save()
        return user


# LOGIN FORM
class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(
            Submit("submit", "Iniciar Sesión", css_class="btn btn-primary")
        )

    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, username=email, password=password
            )
            if self.user_cache is None:
                raise ValidationError(
                    "Usuario o contraseña incorrectos", code="invalid_login"
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


# FORM DE REGISTRO DE DATOS DE CONTACTO
class DatosForm(forms.ModelForm):
    class Meta:
        model = Datos
        fields = ["direccion", "telefono", "email"]
        labels = {"direccion": "Dirección", "telefono": "Teléfono"}
        widgets = {
            "email": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(DatosForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields["email"].initial = self.user.email
            self.helper = FormHelper(self)
            self.helper.add_input(
                Submit("submit", "Guardar", css_class="btn btn-primary")
            )

            try:
                instance = Datos.objects.get(usuario=self.user)
                for field in self.fields:
                    if field != "email":
                        self.fields[field].initial = getattr(instance, field)
            except Datos.DoesNotExist:
                pass

    def save(self, commit=True):
        datos = super().save(commit=False)
        datos.usuario = self.user
        if commit:
            datos.save()
        return datos


# FORM DE REGISTRO DE INMUEBLE
class InmuebleForm(forms.ModelForm):
    imagen = forms.ImageField(required=True)  # Campo para subir la imagen

    class Meta:
        model = Inmueble
        fields = [
            "nombre",
            "direccion",
            "comuna",
            "descripcion",
            "superficie_construida",
            "superficie_total",
            "cantidad_estacionamientos",
            "cantidad_habitaciones",
            "cantidad_banos",
            "tipo_de_inmueble",
            "precio_arriendo",
        ]

        labels = {
            "nombre": "Nombre",
            "direccion": "Dirección",
            "comuna": "Comuna",
            "descripcion": "Descripción",
            "superficie_construida": "Superficie Construida",
            "superficie_total": "Superficie Total",
            "cantidad_estacionamientos": "Cantidad de Estacionamientos",
            "cantidad_habitaciones": "Cantidad de Habitaciones",
            "cantidad_banos": "Cantidad de Baños",
            "tipo_de_inmueble": "Tipo de Inmueble",
            "precio_arriendo": "Precio de Arriendo",
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(InmuebleForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.add_input(
            Submit("submit", "Registrar inmueble", css_class="btn btn-primary")
        )
        if self.user and not self.user.es_arrendador:
            raise forms.ValidationError("No tienes permisos para realizar esta acción")

        # Obtener todas las comunas disponibles
        comunas = Comuna.objects.all().order_by("nombre")
        # Crear una lista de opciones de comuna en formato (id, nombre)
        opciones_comuna = [(comuna.id, comuna.nombre) for comuna in comunas]
        # Actualizar el widget de comuna con las opciones creadas
        self.fields["comuna"].widget = forms.Select(choices=opciones_comuna)

    def save(self, commit=True):
        inmueble = super().save(commit=False)
        instance = isinstance(self.user, Arrendador)
        print("is instance", instance)
        print("Es arrendador", self.user.es_arrendador)
        if isinstance(self.user, Arrendador) and self.user.es_arrendador:
            inmueble.arrendador = self.user
        else:
            raise forms.ValidationError("No tienes permisos para realizar esta acción")
        if commit:
            inmueble.save()
        return inmueble


# FORM DE SOLICITUD DE ARRIENDO
class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ["mensaje"]
        labels = {"mensaje": "Mensaje"}

    def __init__(self, *args, **kwargs):
        self.inmueble = kwargs.pop("inmueble", None)
        self.arrendatario = kwargs.pop("arrendatario", None)
        super(SolicitudForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(
            Submit("submit", "Enviar solicitud", css_class="btn btn-primary")
        )
        if self.inmueble is None or self.arrendatario is None:
            raise forms.ValidationError(
                "Información de inmueble o arrendatario no proporcionada."
            )

    def clean(self):
        cleaned_data = super().clean()
        if self.inmueble and self.arrendatario:
            if self.inmueble.arrendador == self.arrendatario:
                raise forms.ValidationError(
                    "No puedes solicitar arrendar tu propio inmueble"
                )

        if not isinstance(self.arrendatario, Arrendatario):
            raise forms.ValidationError(
                "El usuario debe ser un arrendatario para realizar la solicitud"
            )

        if Solicitud.objects.filter(
            inmueble=self.inmueble, arrendatario=self.arrendatario
        ).exists():
            raise forms.ValidationError(
                "Ya has realizado una solicitud para este inmueble zz"
            )

        return cleaned_data

    def save(self, commit=True):
        solicitud = super().save(commit=False)
        solicitud.inmueble = self.inmueble
        solicitud.arrendatario = self.arrendatario
        if commit:
            solicitud.save()
        return solicitud


# FORM DE BUSQUEDA DE PROPIEDAD


class PropertySearchForm(forms.Form):
    tipo_de_inmueble = forms.ModelChoiceField(
        queryset=TipoDeInmueble.objects.all(),
        required=False,
        label="Tipo de Inmueble",
        empty_label="Todos los tipos",
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label="Región",
        empty_label="Todas las regiones",
    )
    comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.all(),
        required=False,
        label="Comuna",
        empty_label="Todas las comunas",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = (
            False  # Remove this if you want Crispy to generate the <form> tag
        )
        self.helper.layout = Layout(
            *[
                Field(field, css_class="form-control mb-3 custom-field")
                for field in self.fields
            ]
        )

        for field in self.fields:
            self.helper[field].wrap(
                Field, wrapper_class="d-flex flex-column justify-content-end"
            )

        # Establecer valores por defecto
        self.fields["tipo_de_inmueble"].initial = TipoDeInmueble.objects.filter(
            nombre="Todos los tipos"
        ).first()
        region_metropolitana = Region.objects.filter(
            nombre="Región Metropolitana de Santiago"
        ).first()
        self.fields["region"].initial = region_metropolitana
        if region_metropolitana:
            self.fields["comuna"].queryset = Comuna.objects.filter(
                region=region_metropolitana
            ).order_by("nombre")

        # If you want the submit button in the form, uncomment the next line
        # self.helper.add_input(Submit('submit', 'Buscar', css_class='btn btn-primary'))
