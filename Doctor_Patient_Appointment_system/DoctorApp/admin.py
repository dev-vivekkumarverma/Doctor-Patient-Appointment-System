from django.contrib import admin
from .models import DoctorDetails,DoctorLocation,DoctorEductaionalDetails
# Register your models here.

admin.site.register(DoctorDetails)
admin.site.register(DoctorLocation)
admin.site.register(DoctorEductaionalDetails)