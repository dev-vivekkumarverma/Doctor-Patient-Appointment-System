from django.urls import path,include
from .views import all_appointments,create_new_appointment,appointment_by_id,confirm_appointment,mark_complete,mark_cancel
# ,all_appointments_by_date,appointment_by_id
urlpatterns = [
    path("",all_appointments,name="all_appointments_view"),
    # path("<str:date>", all_appointments_by_date,name="all_appointments_by_date_view"),
    path("<int:appointmentId>",appointment_by_id,name="appointment_by_id_view"),
    path("create/<int:doctorId>",create_new_appointment,name="new_appointment_view"),
    path('confirm_appointment/<int:appointmentId>',confirm_appointment,name="appointment_confirmation_view"),
    path('mark_complete/<int:appointmentId>',mark_complete,name="mark_complete_view"),
    path('mark_cancel/<int:appointmentId>',mark_cancel,name="mark_cancel_view"),
]
