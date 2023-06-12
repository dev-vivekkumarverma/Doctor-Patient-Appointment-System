"""Doctor_Patient_Appointment_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static 
from authHandler import urls as authHandlerUrls
from appointmentHandler import urls as appointmentHandlerUrls
from PatientApp import urls as PatientHandlerUrls
from DoctorApp import urls as DoctorAppUrls
from django.shortcuts import render

urlpatterns = [
    path('',lambda request: render(request=request,template_name="index.html"),name="index_page_view"),
    path('admin/', admin.site.urls,name="admin"),
    path('__debug__',include('debug_toolbar.urls'),name="debug"),
    path('users/',include(authHandlerUrls)),
    path('appointments/',include(appointmentHandlerUrls)),
    path('patients/',include(PatientHandlerUrls)),
    path('doctors/',include(DoctorAppUrls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
