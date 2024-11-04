from django.urls import path
from . import views

app_name = 'studentapp'

urlpatterns = [
    path('', views.StudentHomePage, name='StudentHomePage'),
    path('feedback/', views.feedback, name='feedback'),
    path('feedback/success/', views.feedback_success, name='feedback_success'),

]
