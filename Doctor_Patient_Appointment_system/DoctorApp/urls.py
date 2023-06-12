from django.urls import path,include
from .views import all_doctors,doctor_detail_by_id,doctor_self_detail,doctor_self_details_update,edit_location,add_new_location,delete_location_by_id,educational_details

urlpatterns = [
    path("",all_doctors,name="all_doctor_view"),
    path("<int:doctorId>",doctor_detail_by_id,name="doctor_details_by_id_view"),
    path("profile/",doctor_self_detail,name="doctor_self_profile_view"),
    path("profile/update_details/",doctor_self_details_update,name="doctor_self_profile_details_update_view"),
    path("location/edit/<int:locationId>",edit_location,name="edit_location_view"),
    path("location/add/",add_new_location,name="add_new_location_view"),
    path("location/delete/<int:locationId>",delete_location_by_id,name="delete_location_by_id_view"),
    path("educational_details/",educational_details,name="educational_details_view"),
]
