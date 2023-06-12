from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from .models import Appointment
from PatientApp.models import UserProfilePicture, MedicalRecords
from DoctorApp.models import DoctorLocation
from django.http import HttpResponse
from django.utils import timezone
from utility_modules.emailtest import *
import datetime
from django.db import IntegrityError 
from django.contrib import messages
# Create your views here.


@login_required(login_url="user_login_view")
def all_appointments(request):
    doctor=request.user
    try:
        user_profile=UserProfilePicture.objects.get(user=request.user)
    except UserProfilePicture.DoesNotExist:
        user_profile=None
        messages.warning(request=request, message="please upload a profile picture 💔")
    all_appointments=Appointment.objects.filter(date=datetime.date.today(),doctor=doctor)
    total_appointment_count=all_appointments.filter(is_canceled=False).count()
    checked_today=all_appointments.filter(is_completed=True)
    waiting_to_confirm=all_appointments.filter(is_completed=False,is_canceled=False,is_confirm=False)
    confirmed_appointments_for_today=all_appointments.filter(is_completed=False,is_canceled=False,is_confirm=True)
    total_checked_patients=Appointment.objects.filter(is_completed=True,doctor=doctor).count()
    new_appointments=Appointment.objects.filter(date__gte=datetime.date.today(),is_confirm=False,is_canceled=False,doctor=doctor)

    return render(request=request, template_name="doctor_home_page.html",
                  context={"profile_picture":user_profile,
                           "appointments":confirmed_appointments_for_today,
                            "checked_today":checked_today,
                            "waiting_to_confirm":waiting_to_confirm,
                            "total_appointments":total_appointment_count,
                            "new_appointments":new_appointments,
                            "total_checked_patients":total_checked_patients
                            })


@login_required(login_url="user_login_view")
def create_new_appointment(request,doctorId:int):
    try:
        if request.method=="POST":
            location_id=request.POST.get("visiting_location","")
            # print("location details:",location_id, type(location_id))
            location=DoctorLocation.objects.get(id=location_id)
            # print(location)
            doctorGroup=Group.objects.get(name='doctor')
            doctorObject=User.objects.get(pk=doctorId,groups=doctorGroup)
            patient=request.user
            date=request.POST.get("date","")
            reason=request.POST.get("reason","")
            comment=request.POST.get("comment","")
            if all([doctorObject,patient,date,location]):
               
                if datetime.datetime.strptime(date,'%Y-%m-%d').date() >= datetime.date.today():
                    appointmentObject=Appointment()
                    appointmentObject.doctor=doctorObject
                    appointmentObject.date=date
                    appointmentObject.patient=patient
                    appointmentObject.visiting_location=location
                    if reason is not "":
                        appointmentObject.reason=reason
                    if comment is not "":
                        appointmentObject.comments=comment
                    appointmentObject.save()
                    
                    subject="Appointment Request Sent"
                    message=f""" Dear { patient.username },
                    
    Your appointment request with Dr. {doctorObject.username} on date- {date} between - { location.available_from_time } to { location.available_till_time } at visiting_location- { location } have been send successfully.

    We will soon inform you about the cofirmation status.
    Keep checking your registered email.

    Thank You.
                    """
                    send_email(patient.email,subject=subject,body=message)
                    messages.success(request=request,message="appointment request sent successfully ✌️")
                    messages.info(request=request,message="check your email for details 🤗")
                    return redirect(to="patient_profile_view")
                else:
                    messages.error(request=request,message="date should not be already passed 💔")
                    return redirect(to="new_appointment_view",doctorId=doctorId)
            else:
                raise Exception("Some important fields are missing...")
        elif request.method=="GET":
            patient=request.user
            try:
                patient_profile= UserProfilePicture.objects.get(user=patient)
            except UserProfilePicture.DoesNotExist:
                patient_profile=None
                messages.warning(request=request, message="please upload a profile picture ✌️")
            # print(patient_profile)
            doctor=User.objects.get(id=doctorId)
            try:
                doctor_profile=UserProfilePicture.objects.get(user=doctor)
            except UserProfilePicture.DoesNotExist:
                doctor_profile=None
          
            doctor_locations=DoctorLocation.objects.filter(doctor=doctor)
            if doctor_locations.count()==0:
                messages.error(request=request,message="some problem occured 💔\nplease contact the doctor")
                return redirect(to="patient_home_page_view")
            else:    
            # print("doctoe_locations",doctor_locations)
                return render(request=request,template_name="new_appointment.html",context={"doctorId":doctorId,"visiting_locations":doctor_locations,"profile_picture":patient_profile,"doctor_profile":doctor_profile})
    except IntegrityError:
        doctor=User.objects.get(id=doctorId)
        message="You already have a pre-existing appointment request with Dr. {} on same date ✌️".format(doctor.username)
        messages.error(request=request,message=message)
        return redirect(to="new_appointment_view",doctorId=doctorId)
    except Exception as e:
        messages.error(request=request,message=str(e))
        return redirect(to="new_appointment_view",doctorId=doctorId)

@login_required(login_url="user_login_view")
def appointment_by_id(request,appointmentId:int):
    try:
        if request.method=="GET":
            appointmentObject=Appointment.objects.select_related().get(id=appointmentId)
            patient=appointmentObject.patient
            try:
                patient_profile_picture=UserProfilePicture.objects.get(user=patient)
            except UserProfilePicture.DoesNotExist:
                patient_profile_picture=None
            try:
                doctor_profile=UserProfilePicture.objects.get(user=request.user)
            except UserProfilePicture.DoesNotExist:
                doctor_profile=None
            all_medical_files=MedicalRecords.objects.filter(user=patient)
            # print(all_medical_files)
            return render(request=request,template_name="appointment_details.html",context={"appointment":appointmentObject,"medical_files":all_medical_files,"profile_picture":doctor_profile,"patient_profile_picture":patient_profile_picture})
    except Exception as e:
        messages.error(request=request,message="error occured 🥹")
        if request.user.groups.filter(name="patient").exists():
            redirect(to="doctor_self_profile_view")
        elif request.user.groups.filter(name="doctor").exists():
            redirect(to="all_appointments_view")
        else:
            return render(request=request,template_name="message.html",context={"message":str(e)})
    

@login_required(login_url="user_login_view")
def confirm_appointment(request,appointmentId):
    try:
        if  request.user.groups.filter(name="doctor").exists():
            appointment=Appointment.objects.select_related().get(id=appointmentId, doctor=request.user)
            if appointment.is_confirm is False and appointment.is_canceled is False and appointment.is_completed is False:
                appointment.is_confirm=True
                appointment.save()
                subject="Appoinment Confirmed"
                message=f"""
Hey { appointment.patient.username }, 

Your appointment with Dr. { request.user.username } on {appointment.date} in visiting hours - {appointment.visiting_location.available_from_time} - {appointment.visiting_location.available_till_time} is confirmed !

Thank you for the patience.
                """
                send_email(appointment.patient.email,subject=subject,body=message)
                messages.success(request=request, message="appointment confirmed successfully ✌️")
                return redirect(to="all_appointments_view")
            else:
                raise Exception("Either this appointment is completed or have been canceled before 😯")
        else:
            raise Exception("operation Not allowed 💔")    
    except Exception as e:
        messages.error(request=request, message=str(e))
        return redirect(to="appointment_by_id_view",appointmentId=appointmentId)


@login_required(login_url="user_login_view")
def mark_complete(request,appointmentId:int):
    try:
        if request.user.groups.filter(name="doctor").exists():
            appointment=Appointment.objects.get(id=appointmentId,doctor=request.user)
            appointment.mark_complete()
            messages.success(request=request, message="appointment marked completed successfully ✌️")
            return redirect(to="all_appointments_view")
        else:
            raise Exception("operation not allowed 💔")
    except Exception as e:
        messages.error(request=request, message=str(e))
        return redirect(to="appointment_by_id_view",appointmentId=appointmentId)
    
@login_required(login_url="user_login_view")
def mark_cancel(request,appointmentId:int):
    try:
        if request.user.groups.filter(name="doctor").exists():
            appointment=Appointment.objects.get(id=appointmentId,doctor=request.user)
            if appointment.mark_cancel():
                messages.success(request=request,message="appointment canceled successfully ✌️")
                return redirect(to="all_appointments_view")
            else:
                raise Exception("this appointment is already canceled or completed 🤗")
        else:
            raise Exception("operation not allowed 💔 ")
    except Exception as e:
        messages.error(request=request, message=str(e))
        return redirect(to="appointment_by_id_view",appointmentId=appointmentId)