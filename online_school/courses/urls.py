from django.urls import path, include, reverse_lazy
from .views import *

urlpatterns = [
    path('courses_list/', CoursesListView.as_view(), name='courses_list'),
    path('user_courses_list/', UserCoursesListView.as_view(), name='user_courses_list'),
    path('course_detail/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('course_detail/<int:pk>/students_list/', StudentsListView.as_view(), name='students_list'),
    path('add_course/', AddCourseView.as_view(), name='add_course'),
    path('edit_course/<int:pk>/', EditCourseView.as_view(), name='edit_course'),


    path('course/<int:pk>/add_lesson/', AddLessonView.as_view(), name='add_lesson'),
    path('course/<int:course_pk>/lesson/<int:lesson_pk>/', LessonDetailView.as_view(), name='lesson_detail')
]