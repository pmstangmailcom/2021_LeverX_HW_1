from django.urls import path
from .views import *


app_name = "courses"

urlpatterns = [

    path('register/', UserCreate.as_view(), name='account-create'),

    path('courses/', CourseListView.as_view(), name='course_list'),
    path('course/<int:pk>', CourseDetailView.as_view(), name='course_detail'),
    path('course/', CourseCreateView.as_view(), name='course_create'),
    path('update/<int:pk>', CourseUpdateDeleteView.as_view(), name='course_update'),

]