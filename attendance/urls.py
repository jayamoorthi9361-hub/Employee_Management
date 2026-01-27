from django.urls import path
from .views import CheckInView, CheckOutView, AttendanceHistoryView, TodaysAttendanceView

urlpatterns = [
    path('check-in/', CheckInView.as_view(), name='check_in'),
    path('check-out/', CheckOutView.as_view(), name='check_out'),
    path('history/', AttendanceHistoryView.as_view(), name='attendance_history'),
    path('today/', TodaysAttendanceView.as_view(), name='todays_attendance'),
]
