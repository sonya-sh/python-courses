from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from .models import Course

def is_teacher(user):
    return user.groups.filter(name='Teachers').exists()

teacher_required = user_passes_test(is_teacher)


def is_student(user):
    return user.groups.filter(name='Students').exists()

student_required = user_passes_test(is_student)


def is_course_teacher(user, course_id):
    course = Course.objects.get(pk=course_id)
    return user.groups.filter(name='Teachers').exists() and user in course.teacher.all()

#course_teacher_required = user_passes_test(is_course_teacher)
#def course_teacher_required(course_id):
#    return user_passes_test(lambda user: is_course_teacher(user, course_id))