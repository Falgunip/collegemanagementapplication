from django.contrib import admin

from administrator.models import Studentapplication, Studentregistration, Staffregistration, Department
from . import models
# Register your models here.

admin.site.register(Studentapplication)
admin.site.register(Studentregistration)
admin.site.register(Staffregistration)
admin.site.register(Department)
