from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from DoctorApp.models import DoctorDetails
from django.contrib import messages
from django.http import HttpResponse
from utility_modules.emailtest import *

# Create your views here.


def userRegistration(request):
    try:
        if request.method=="GET":
            return render(request=request,template_name='user_registration.html')
        elif request.method=="POST":
            # print(request.POST)
            password=request.POST.get("password","")
            confirm_password=request.POST.get("confirm_password","")
            if password==confirm_password:
                username=request.POST.get("username","")
                email=request.POST.get("email","")
                group=request.POST.get("group","patient")
                # print(username,email,group)
                if all([password,confirm_password,username,email,group]):
                    newUser=User.objects.create_user(username=username,password=password,email=email)
                    if group=="doctor":
                        newUser.is_active=False
                    else:
                        newUser.is_active=True
                    newUser.save()
                    group_object,_=Group.objects.get_or_create(name=group)
                    newUser.groups.add(group_object)
                    if group=='doctor' and newUser.is_active is False:
                        message=f"""
Dear {username},
    Your registration has been successfull...
    activation code : 567232
    This is your account activation link... 
    http://localhost:8000/users/activate/{newUser.pk}
                    """
                        subject="DPA System varification success"
                        # email_thread=threading.Thread(group=None,target=send_email,args=[email,subject,message])
                        # email_thread.start()
                        send_email(email,subject=subject,body=message)
                    elif group=='patient':
                        # make opt based activation system for patient user
                        pass
                    # print("registrations successful...")
                    messages.success(request=request, message="registration successful")
                    return redirect(to='user_login_view')
                else:
                    raise Exception("some fields are missing")
            else:
                raise Exception("Password and confirm_password do not match..")
    except Exception as e:
        messages.error(request=request,message=str(e))
        return  redirect(to="user_registration_view")



def userLogin(request):
    try:
        if request.method=="GET":
            return render(request=request,template_name="user_login.html")
        elif request.method=="POST":
            username=request.POST.get("username","")
            password=request.POST.get("password","")
            # print("username:",username)
            # print("password:",password)
            if all([username,password]):
                authenticatedUser=authenticate(username=username,password=password)
                # print(authenticatedUser)
                # messages.warning(request=request, message="login failed 💔")
                if authenticatedUser != None:
                    if authenticatedUser.is_active is True:
                        login(request=request,user=authenticatedUser)
                        messages.success(request=request, message="login successful ✌️")
                        if request.user.groups.filter(name="patient").exists():
                            return redirect(to="patient_home_page_view")
                        elif request.user.groups.filter(name="doctor").exists():
                            return redirect(to="all_appointments_view")
                        else: 
                            return HttpResponse('login successfull...')
                    else:
                        messages.error(request=request, message=f"activate your account... \ncheck your email for activation Link...\n check mail from doctorpatientappointmentsystem@gmail.com\nThank you...")
                        return redirect(to="user_login_view")
                else:
                    messages.error(request=request,message="login failed..check username and password and try again ✌️")
                    return redirect(to="user_login_view")
            else:
                messages.error(request=request,message="some fields missing 😐")
                return redirect(to="user_login_view")
    except Exception as e:
        messages.error(request=request, message="login failed 💔")
        return redirect(to="user_login_view")
        
@login_required(login_url="user_login_view")
def userLogout(request):
    user=request.user.username
    logout(request=request)
    message= "{} has been successfully Logged out. ".format(str(user).capitalize())
    messages.success(request=request,message=message)
    return redirect(to="index_page_view")



def account_activation(request,userId:int):
    try:
        user=User.objects.get(pk=userId)
        if user is not None:
            if user.is_active is False:
                user.is_active=True
                user.save()
                message=f" Congratualations your DPA-System account has been successfully activated ! "
                subject="no-reply"
                # mail_thread=threading.Thread(group=None,target=send_email,args=[user.email,subject,message])
                # mail_thread.start()
                send_email(user.email,subject=subject,body=message)
                messages.success(request=request,message="account activated successfully 🥳")
                return redirect(to="user_login_view")
            else:
                raise Exception("Already actived account can not be re-activated ! ✌️")
        else:
            raise Exception("Invalid User 🤔")
    except Exception as e:
        messages.error(request=request,message=str(e))
        return redirect(to="user_login_view")
            
