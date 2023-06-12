from django.urls import path,include
from .views import userRegistration,userLogin,userLogout,account_activation

urlpatterns = [
    path('',userRegistration,name="user_registration_view"),
    path('login/',userLogin,name='user_login_view'),
    path("logout/",userLogout,name="user_logout_view"),
    path("activate/<int:userId>",account_activation,name="user_account_activation_view"),
]
