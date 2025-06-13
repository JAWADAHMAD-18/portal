from django.urls import path,include
from. import views

urlpatterns = [
    path('base/',views.wow),
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('/signup',views.signup,name='signup'),
    path('career/',views.career,name='ass_index'),
    path('logout/', views.logout, name='logout'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('appointment/<int:teacher_id>/', views.appointment, name='appointment'),
    path('career-report/review/<int:report_id>/',views.review_career_report, name='review_career_report'),
    path('career-report/list/', views.career_report_list, name='career_report_list'),
    path('my-career-report/',views.view_my_career_report, name='my_career_report'),
    path('dashboard/',views.student_dashboard,name='dashboard'),
    path('feedback/<int:teacher_id>/',views.give_feedback,name='feedback'),
    path('appointment/confirmation/<int:appointment_id>/', views.appointment_confirmation, name='appointment_confirmation'),
    path('teacher/my-appointments/', views.teacher_appointments, name='teacher_appointments'),
    path('appointments/<int:appointment_id>/accept/', views.accept_appointment, name='accept_appointment'),




]