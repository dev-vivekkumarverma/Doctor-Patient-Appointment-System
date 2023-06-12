from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PatientApp.models import UserProfilePicture
# Create your models here.
# Gender_choics=(("male","male"),("female","female"),("others","others"))

class DoctorEductaionalDetails(models.Model):
    doctor=models.ForeignKey(User,on_delete=models.DO_NOTHING,unique=True)
    ug_course=models.CharField(max_length=50,null=True,blank=True)
    ug_institute=models.CharField(max_length=100,blank=True,null=True)
    pg_course=models.CharField(max_length=50,null=True,blank=True)
    pg_institute=models.CharField(max_length=100,blank=True,null=True)
    years_of_experience=models.IntegerField(max_length=3,default=0)

    def get_edit_eduational_details(self):
        return reverse("educational_details_view")
    
    def get_add_eduational_details(self):
        return reverse("educational_details_view")
    
    def __str__(self):
        return "Dr. {}'s educational details".format(self.doctor.username)

class DoctorDetails(models.Model):
    profile=models.ForeignKey(UserProfilePicture,on_delete=models.DO_NOTHING)
    # gender=models.CharField(choices=Gender_choics, default="male")
    specialization_area=models.CharField(max_length=300, default="general",blank=True)
    specialization=models.CharField(max_length=300,blank=True,null=True)
    location_details=models.CharField(max_length=300)
    phone_number=models.CharField(max_length=16, null=False,unique=True)
    is_varified_phone=models.BooleanField(default=False)
    available_from_time=models.TimeField()
    available_till_time=models.TimeField()
    is_available=models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("doctor_details_by_id_view", kwargs={"doctorId": self.profile.user.pk})
    def __str__(self):
        return "Dr. {} 's details".format(self.profile.user.username)

    
class DoctorLocation(models.Model):
    doctor=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    street=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=30,null=True)
    state=models.CharField(max_length=30,null=True)
    pincode=models.DecimalField(null=True,max_digits=6,decimal_places=0)
    available_from_time=models.TimeField()
    available_till_time=models.TimeField()
    def get_delete_url(self):
        return reverse("delete_location_by_id_view",kwargs={"locationId":self.pk})
    def get_edit_url(self):
        return reverse("edit_location_view",kwargs={"locationId":self.pk})
    def __str__(self) -> str:
        return f"{self.street}, {self.city}, {self.state} - {self.pincode}"
    
    

