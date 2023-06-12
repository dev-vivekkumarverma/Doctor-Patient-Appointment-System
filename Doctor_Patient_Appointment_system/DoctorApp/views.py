from django.shortcuts import render,redirect
from .models import DoctorDetails,DoctorLocation,DoctorEductaionalDetails
from PatientApp.models import UserProfilePicture
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from utility_modules.emailtest import *
from django.contrib import messages
# Create your views here.

@login_required(login_url="user_login_view")
def all_doctors(request):
    user=request.user
    user_profile=UserProfilePicture.objects.get(user=user)
    all_doctors=DoctorDetails.objects.select_related().all()
    if all_doctors.count()==0:
        messages.info("no doctor present.")
    return render(request=request,template_name="all_doctors.html",context={"doctors":all_doctors,"profile_picture":user_profile})

@login_required(login_url="user_login_view")
def doctor_detail_by_id(request,doctorId:int):
    try:
        patient=request.user
        try:
            user_profile=UserProfilePicture.objects.select_related().get(user=patient)
        except UserProfilePicture.DoesNotExist:
            user_profile=None
            messages.warning(request=request, message="please upload profile picture ✌️")
        doctor=User.objects.get(id=doctorId)
        doctorProfile=UserProfilePicture.objects.get(user=doctor)
        doctor_Details=DoctorDetails.objects.select_related().get(profile=doctorProfile)
        doctor_locations=DoctorLocation.objects.filter(doctor=doctor)
        try:
            doctor_educational_details=DoctorEductaionalDetails.objects.get(doctor=doctor)
        except DoctorEductaionalDetails.DoesNotExist:
            doctor_educational_details=None

        return render(request=request,template_name="doctor_detail_view_page.html",context={"doctor":doctor_Details,"profile_picture":user_profile,"visiting_locations":doctor_locations,"doctor_educational_details":doctor_educational_details})
    except Exception as e:
        messages.error(request=request, message='some error occured 🥹')
        return redirect(to="patient_home_page_view")
    
@login_required(login_url="user_login_view")
def doctor_self_detail(request):
    try:
        if request.method=="GET":
            doctor=request.user
            doctor_profile=UserProfilePicture.objects.get(user=doctor)
            doctor_details=DoctorDetails.objects.select_related().get(profile=doctor_profile)
            try:
                doctor_locations=DoctorLocation.objects.filter(doctor=doctor)
            except DoctorLocation.DoesNotExist:
                doctor_locations=None
                messages.warning(request=request,message="please add at least a visiting location 😐")
            try:
                doctor_educational_details=DoctorEductaionalDetails.objects.get(doctor=doctor)
            except DoctorEductaionalDetails.DoesNotExist:
                doctor_educational_details=None
                messages.error(request=request,message="your educational details not found 💔")
                messages.warning(request=request,message="please add your eduacatioal details 💔")
            return render(request=request,template_name="doctor_profile_details.html",context={"doctor":doctor_details,"profile_picture":doctor_profile,"doctor_locations":doctor_locations,"doctor_educational_details":doctor_educational_details})
        else:
            messages.warning(request=request,message="{} method is not allowed ✌️".format(request.method))
            return redirect(to="all_appointments_view")
    except Exception as e:
        messages.error(request=request, message='some error occured 🥹')
        return redirect(to="all_appointments_view")
    

@login_required(login_url="user_login_view")
def doctor_self_details_update(request):
    try:
        if request.method=="GET":
            doctor=request.user
            doctor_profile=UserProfilePicture.objects.get(user=doctor)
            doctor_details=DoctorDetails.objects.select_related().get(profile=doctor_profile)
            return render(request=request,template_name="doctor_details_edit_page.html",context={"doctor":doctor_details,"profile_picture":doctor_profile})
        elif request.method=="POST":
            doctor=request.user
            old_email=request.user.email
            email=old_email
            doctor_profile=UserProfilePicture.objects.get(user=doctor)
            doctor_details=DoctorDetails.objects.select_related().get(profile=doctor_profile)
            # new data
            new_specialization_area=request.POST.get("specialization_area","")
            new_specialization=request.POST.get("specialization","")
            new_available_from_time=request.POST.get("available_from_time","")
            new_available_till_time=request.POST.get("available_till_time","")
            new_phone_number=request.POST.get("phone_number","")
            new_email=request.POST.get("email","")
            new_location_details=request.POST.get("location_details","")
            new_is_available=request.POST.get("is_available","")
            #let's check the chnages and save then one by one
            doctor_details.location_details=new_location_details
            doctor_details.specialization=new_specialization
            doctor_details.specialization_area=new_specialization_area
            change_message=""
            if new_is_available == 'true':
                new_is_available=True
            else:
                new_is_available=False
            if doctor_details.is_available!=new_is_available:
                doctor_details.is_available=new_is_available
                change_message+="* Your availability status have been changed."
            doctor_details.phone_number=new_phone_number
            if new_available_from_time !="":
                doctor_details.available_from_time=new_available_from_time
                change_message+=f"* Your start visiting time have been changed to {new_available_from_time}."
            if new_available_till_time !="":
                doctor_details.available_till_time=new_available_till_time
                change_message+=f"* Your end visiting time have been changed to {new_available_till_time}."
            doctor_details.save()
            if old_email !=new_email:
                doctor.email=new_email
                doctor.save()
                email=new_email
                change_message+=f"* Your email has been changed from {old_email} to {new_email}."
            subject="Profile Details Changed"    
            message="your profile changes have been saved successfully. following changes have been made:-\n"+change_message
            send_email(email_receiver=email,subject=subject,body=message)
            messages.success(request=request, message="Details updated successfully ✌️")
            return redirect(to="doctor_self_profile_view")

    except Exception as e:
        messages.error(request=request,message="some error has been occured 🥹")
        return redirect(to="doctor_self_profile_details_update_view")
    

   


@login_required(login_url="user_login_view")
def edit_location(request,locationId:int):
    try:
        if request.method=="POST":
            location= DoctorLocation.objects.get(id=locationId)
            location.city=request.POST.get("city","")
            location.state=request.POST.get("state","")
            location.street=request.POST.get("street","")
            location.pincode=request.POST.get("pincode","")
            location.available_from_time=request.POST.get("available_from_time","")
            location.available_till_time=request.POST.get("available_till_time","")
            location.save()
            messages.success(request=request, message="location update successfull.")
            return redirect(to="doctor_self_profile_view")
        else:
            doctor= request.user
            location= DoctorLocation.objects.get(id=locationId)
            try:
                doctor_profile_picture= UserProfilePicture.objects.get(user=doctor)
            except UserProfilePicture.DoesNotExist:
                doctor_profile_picture=None
                messages.warning(request=request, message="please upload a profile picture.🤗")

            return render(request=request,template_name="doctor_location_edit.html",context={"profile_picture":doctor_profile_picture,"location_details":location})

    except Exception as e:
        messages.error(request=request, message="Error occured 🥹")
        return redirect(to="doctor_self_profile_view")
    
@login_required(login_url="user_login_view")
def add_new_location(request):
    try:
        if request.method=="GET":
            doctor= request.user
            try:
                doctor_profile_picture= UserProfilePicture.objects.get(user=doctor)
            except UserProfilePicture.DoesNotExist:
                doctor_profile_picture=None
                messages.warning(request=request,message="Please upload a profile picture.")
            return render(request=request,template_name="doctor_add_new_location.html",context={"profile_picture":doctor_profile_picture})
        elif request.method=="POST":
            doctor=request.user
            if DoctorLocation.objects.filter(doctor=doctor).count() <3:

                city=request.POST.get("city","")
                state=request.POST.get("state","")
                street=request.POST.get("street","")
                pincode=request.POST.get("pincode","")
                available_from_time=request.POST.get("available_from_time","")
                available_till_time=request.POST.get("available_till_time","")
                if all([city,state,street,pincode,available_from_time,available_till_time,doctor]):
                    location= DoctorLocation()
                    location.doctor=doctor
                    location.city=city
                    location.state=state
                    location.street=street
                    location.pincode=pincode
                    location.available_from_time=available_from_time
                    location.available_till_time=available_till_time
                    location.save()
                    messages.success(request=request,message="Visiting location added successfully🤗")
                    return redirect(to="doctor_self_profile_view")
                else:
                    messages.error(request=request, message="some fields are missing 💔")
                    raise redirect(to="add_new_location_view")
            else:
                messages.error(request=request, message="maximum visiting location limit has already been reached ⏹️")
                return redirect(to="doctor_self_profile_view")
    except Exception as e:
        messages.error(request=request,message="some error occured 💔")
        return redirect(to="add_new_location_view")
    

@login_required(login_url="user_login_view")
def delete_location_by_id(request,locationId:int):
    doctor=request.user
    location=DoctorLocation.objects.get(id=locationId)
    if location.doctor==doctor:
        messages.success(request=request, message="location deleted successfully ✌️")
        location.delete()
    return redirect(to="doctor_self_profile_view")


@login_required(login_url="user_login_view")
def educational_details(request):
    try:
        doctor=request.user
        if request.method=="POST":
            ug_course=request.POST.get("ug_course","")
            ug_institute=request.POST.get("ug_institute","")
            pg_course=request.POST.get("pg_course","")
            pg_institute=request.POST.get("pg_institute","")
            years_of_experience=request.POST.get("years_of_experience","")
            doctor_educational_details,new=DoctorEductaionalDetails.objects.get_or_create(doctor=doctor)
            doctor_educational_details.ug_course=ug_course
            doctor_educational_details.ug_institute=ug_institute
            doctor_educational_details.pg_course=pg_course
            doctor_educational_details.pg_institute=pg_institute
            doctor_educational_details.years_of_experience=years_of_experience
            doctor_educational_details.save()
            messages.success(request=request,message="Your educational details added successfully 🤗")
            return redirect(to="doctor_self_profile_view")

        elif request.method=="GET":
            try:
                profile_picture=UserProfilePicture.objects.get(user=doctor)
            except UserProfilePicture.DoesNotExist:
                profile_picture=None
                messages.warning(request=request,message="please your upload profile picture ✌️")
            try:
                doctor_educational_details=DoctorEductaionalDetails.objects.get(doctor=doctor)
            except DoctorEductaionalDetails.DoesNotExist:
                doctor_educational_details=None
                messages.warning(request=request,message="please upload educational details ✌️")
            return render(request=request,template_name="edit_doctor_educational_details.html",context={"doctor_educational_details":doctor_educational_details,"profile_picture":profile_picture})
        else:
            messages.warning(request=request,message="{} method is not allowed 🤔".format(request.method))
            return redirect(to="doctor_self_profile_view")
    except Exception as e:
        messages.error(request=request,message="some error occured 💔")
        print(str(e))
        return redirect(to="doctor_self_profile_view")
    

    # "some error occured 💔"