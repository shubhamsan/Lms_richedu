from django.urls import path,include
from django.conf.urls import url

from . import views

urlpatterns = [
   
    path('',views.student_detail,name='student_detail'),

]