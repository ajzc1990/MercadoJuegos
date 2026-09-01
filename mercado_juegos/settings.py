"""
Django settings for mercado_juegos project.
"""

from pathlib import Path
from decouple import config, Csv

# -----------------------------------------------------------------------------
# 1. RUTAS BASE Y SEGURIDAD
# -----------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config(
    'SECRET_KEY', 
    default='django-insecure-clave-de-desarrollo-mercado-juegos-local'
)

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS', 
    default='127.0.0.1,localhost,0.0.0.0', 
    cast=Csv()
)

CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS', 
    default='http://127.0.0.1,http://localhost', 
    cast=Csv()
)


# -----------------------------------------------------------------------------
# 2. APLICACIONES INSTALADAS
# -----------------------------------------------------------------------------

INSTALLED_APPS = [
    # Aplicaciones nativas de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Aplicaciones del proyecto
    'home',
    'cuentas',
    'publicaciones',
    'ventas',
    'entregas',
]


# -----------------------------------------------------------------------------
# 3. MIDDLEWARE
# -----------------------------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mercado_juegos.urls'


# -----------------------------------------------------------------------------
# 4. PLANTILLAS / TEMPLATES
# -----------------------------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'mercado_juegos.wsgi.application'


# -----------------------------------------------------------------------------
# 5. BASE DE DATOS (PostgreSQL con fallback SQLite)
# -----------------------------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': config('DB_NAME', default='mercado_juegos_db'),
        'USER': config('DB_USER', default='mercado_user'),
        'PASSWORD': config('DB_PASSWORD', default='mercado_pass_segura'),
        'HOST': config('DB_HOST', default='db'),
        'PORT': config('DB_PORT', default='5432'),
    }
}


# -----------------------------------------------------------------------------
# 6. VALIDACIÓN DE CONTRASEÑAS
# -----------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# -----------------------------------------------------------------------------
# 7. IDIOMA Y ZONA HORARIA
# -----------------------------------------------------------------------------

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Argentina/Tucuman'

USE_I18N = True

USE_TZ = True


# -----------------------------------------------------------------------------
# 8. ARCHIVOS ESTÁTICOS Y MULTIMEDIA
# -----------------------------------------------------------------------------

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# -----------------------------------------------------------------------------
# 9. RUTAS DE AUTENTICACIÓN
# -----------------------------------------------------------------------------

LOGIN_URL = 'cuentas:login'
LOGIN_REDIRECT_URL = 'home:inicio'
LOGOUT_REDIRECT_URL = 'cuentas:despedida'


# -----------------------------------------------------------------------------
# 10. CLAVE PRIMARIA
# -----------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# -----------------------------------------------------------------------------
# 11. MERCADO PAGO SDK
# -----------------------------------------------------------------------------

MERCADOPAGO_ACCESS_TOKEN = config(
    'MERCADOPAGO_ACCESS_TOKEN', 
    default='APP_USR-3626438108805929-073017-26ee1f7c708a9a5a0bd2370e19806d3c-3580269154'
)


# -----------------------------------------------------------------------------
# 12. CONFIGURACIÓN DE CORREO ELECTRÓNICO (SMTP Gmail)
# -----------------------------------------------------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='agustinzelayacossio@gmail.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='wvjj razf eedc xxjg')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='Mercado Juegos <agustinzelayacossio@gmail.com>')