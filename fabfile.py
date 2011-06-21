from armstrong.dev.tasks import *

settings = {
    'DEBUG': True,
    'INSTALLED_APPS': (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'armstrong.utils.backends',
        'lettuce.django',
        'south',
        'mptt',
    ),
    'SITE_ID': 1,
}

full_name = "armstrong.utils.backends"
main_app = "backends"
tested_apps = (main_app, )
