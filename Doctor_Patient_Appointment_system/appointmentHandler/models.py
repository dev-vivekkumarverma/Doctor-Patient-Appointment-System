from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from DoctorApp.models import DoctorLocation
from django.utils import timezone
# Create your models here.


class Appointment(models.Model):
    doctor=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="doctor")
    patient=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="patient")
    visiting_location=models.ForeignKey(DoctorLocation,on_delete=models.DO_NOTHING,related_name="appointment")
    date=models.DateField(null=True,blank=True)
    reason=models.CharField(max_length=500,default="checkup")
    comments=models.TextField(null=True)
    created_on=models.DateTimeField(auto_now_add=True)
    is_confirm=models.BooleanField(default=False,null=True)
    is_canceled=models.BooleanField(default=False,null=True)
    is_completed=models.BooleanField(default=False,null=True)
    class Meta:
       unique_together=("patient","doctor","date") 

    def get_absolute_url(self):
        return reverse("appointment_by_id_view", args=[self.pk])
    def get_mark_complete_url(self):
        return reverse("mark_complete_view",args=[self.pk])
    def get_mark_cancel_url(self):
        return reverse("mark_cancel_view",args=[self.pk])
    
    def get_mark_confirm_url(self):
        return reverse("appointment_confirmation_view",args=[self.pk])
    def __str__(self):
        return "{} - Dr. {} - {} for {}".format(self.patient.username,self.doctor.username,self.date,self.reason)
    
    def mark_complete(self):
        if self.is_canceled==False and self.is_completed==False and self.is_confirm==True:
            self.is_completed=True
            self.save()
    def mark_cancel(self):
        if self.is_completed == False and self.is_canceled == False:
            self.is_canceled=True
            self.save()
            return True
        return False
        

