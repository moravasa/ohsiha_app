from django.contrib import admin


# Register your models here.
from .models import Kysymys
from .models import Juna

admin.site.register(Kysymys)
admin.site.register(Juna)
