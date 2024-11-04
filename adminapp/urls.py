from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.projecthomepage, name='projecthomepage'),
    path('printpagecall/', views.printpagecall, name='printpagecall'),
    path('printpagelogic/', views.printpagelogic, name='printpagelogic'),
    path('exceptionpagecall/', views.exceptionpagecall, name='exceptionpagecall'),
    path('exceptionpagelogic/', views.exceptionpagelogic, name='exceptionpagelogic'),
    path('randompagecall/', views.randompagecall, name='randompagecall'),
    path('randomlogic/', views.randomlogic, name='randomlogic'),
    path('calculatorlogic/', views.calculatorlogic, name='calculatorlogic'),
    path('add_task/', views.add_task, name='add_task'),
    path('upload_file/',views.upload_file, name='upload_file'),
    path('<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('UserLoginLogic/', views.UserLoginLogic, name='UserLoginLogic'),
    path('UserLoginPageCall/', views.UserLoginPageCall, name='UserLoginPageCall'),
    path('UserRegisterLogic/', views.UserRegisterLogic, name='UserRegisterLogic'),
    path('UserRegisterPageCall/', views.UserRegisterPageCall, name='UserRegisterPageCall'),
    path('logout/', views.logout, name='logout'),
    path('add_student/',views.add_student, name='add_student'),
    path('student_list/', views.student_list, name='student_list'),
    path('daytimepagelogic/', views.daytimepagelogic, name='daytimepagelogic'),
    path('daytimepagecall/', views.daytimepagecall, name='daytimepagecall'),
    path('add_contact/', views.add_contact, name='add_contact'),
    path('contact_list/', views.contact_list, name='contact_list'),
    path('delete_contact/<int:contact_id>/', views.delete_contact, name='delete_contact')

]