from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from .models import *
from .permissions import teacher_required, student_required, is_course_teacher
from .forms import CourseCreationForm, SubscribeForm, CourseEditForm, LessonCreationForm, LessonDoneForm

class CoursesListView(View):

    def get(self, request):
        courses = Course.objects.all()
        user = request.user
        context = {
            'courses_list': courses,
            'can_add_course': user.groups.filter(name='Teachers').exists(), # True/False
        }
        return render(request, 'courses/courses_list.html', context)
    
class UserCoursesListView(View):

    def get(self, request):
        enrollments = Enrollment.objects.filter(student=request.user) # pk
        student_courses = [enrollment.course for enrollment in enrollments]
        teacher_courses = Course.objects.filter(teacher__in=[request.user])
        context = {
            'is_teacher': request.user.groups.filter(name='Teachers').exists(), # True/False
            'is_student': request.user.groups.filter(name='Students').exists(), # True/False
            'student_courses_list': student_courses,
            'teacher_courses_list': teacher_courses
        }
        return render(request, 'courses/user_courses_list.html', context)
    
class CourseDetailView(View):

    def get(self, request, pk):
        course = Course.objects.get(pk=pk)
        lessons = course.lessons.all()
        teachers = course.teacher.all()
        try:
            enrollment = Enrollment.objects.get(student=request.user, course=pk)
            percent = enrollment.get_completion_percentage()
        except Enrollment.DoesNotExist:
            percent = None  
        form = SubscribeForm()
        context = {
            'course': course,
            'lessons_list': lessons,
            'teachers': teachers,
            'percent': percent,
            'form': form,
            'can_subscribe': request.user.groups.filter(name='Students').exists(), # True/False
            'can_edit': request.user.groups.filter(name='Teachers').exists()
        }
        return render(request, 'courses/course_detail.html', context)
    
    @method_decorator(student_required)
    def post(self, request, pk):
        course = Course.objects.get(pk=pk)
        lessons = course.lessons.all()
        user = request.user
        form = SubscribeForm(request.POST)

        if Enrollment.objects.filter(student=user, course=course).exists():
                messages.warning(request, "Вы уже подписаны на этот курс.")
                return redirect('course_detail', pk=pk)
        
        if form.is_valid():
            Enrollment.objects.create(student=user, course=course)
            return redirect('course_detail', pk=pk)
        
        context = {
            'course': course,
            'lessons_list': lessons,
            'form': form,
            'can_subscribe': request.user.groups.filter(name='Students').exists(), # True/False
        }
        return render(request, 'courses/course_detail.html', context)

@method_decorator(teacher_required, name='dispatch')
class AddCourseView(View):

    def get(self, request):
        form = CourseCreationForm()
        context = {
            'form': form
        }
        return render(request, 'courses/add_course.html', context)

    def post(self, request):
        form = CourseCreationForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.save() 

            # сохранить множественные отношения (выранных учителей курса)
            form.save_m2m()

            return redirect('courses_list')
        else:
            context = {
                'form': form
            }
            return render(request, 'courses/add_course.html', context)

class EditCourseView(View):
    
    def dispatch(self, request, *args, **kwargs):
        course_id = self.kwargs['pk']  # Получаем course_id из URL
        if not is_course_teacher(request.user, course_id):
            return HttpResponseForbidden()  # Возвращаем 403 Forbidden, если пользователь не является преподавателем курса
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, pk):
        course = Course.objects.get(pk=pk)
        form = CourseEditForm(instance=course)
        context = {
            'form': form
        }
        return render(request, 'courses/edit_course.html', context)
    
    def post(self, request, pk):
        course = Course.objects.get(pk=pk)
        form = CourseEditForm(request.POST, instance=course)

        if form.is_valid():
            form.save()
            messages.success(request, "Курс успешно обновлен.")
            return redirect('course_detail', pk=pk)

        context = {
            'course': course,
            'form': form,
        }
        return render(request, 'courses/edit_course.html', context)

# @method_decorator(teacher_required, name='dispatch')
class AddLessonView(View):

    def dispatch(self, request, *args, **kwargs):
        course_id = self.kwargs['pk']  # Получаем course_id из URL
        if not is_course_teacher(request.user, course_id):
            return HttpResponseForbidden()  # Возвращаем 403 Forbidden, если пользователь не является преподавателем курса
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        course = Course.objects.get(pk=pk)
        form = LessonCreationForm()
        context = {
            'course': course,
            'form': form
        }
        return render(request, 'courses/add_lesson.html', context)

    def post(self, request, pk):
        course = Course.objects.get(pk=pk)
        form = LessonCreationForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('course_detail', pk=pk)
        else:
            context = {
            'course': course,
            'form': form
        }
        return render(request, 'courses/add_lesson.html', context)
    
class LessonDetailView(View):

    def get(self, request, lesson_pk, course_pk):
        course = Course.objects.get(pk=course_pk)
        lesson = Lesson.objects.get(pk=lesson_pk)
        context = {
            'lesson': lesson,
            'course': course,
            'can_mark_lesson_as_completed': request.user.groups.filter(name='Students').exists(),
        }
        return render(request, 'courses/lesson_detail.html', context)
    
    def post(self, request, lesson_pk, course_pk):
       
        enrollment = Enrollment.objects.get(student=request.user, course=course_pk)
        form = LessonDoneForm(request.POST)
        if form.is_valid():
            if enrollment.completed_lessons.filter(pk=lesson_pk).exists():
                enrollment.mark_lesson_as_not_completed(lesson_pk)
            else:
                enrollment.mark_lesson_as_completed(lesson_pk)
            return redirect('lesson_detail', course_pk=course_pk, lesson_pk=lesson_pk)
        else:
            return render(request, 'courses/lesson_detail.html', {'form': form})


@method_decorator(teacher_required, name='dispatch') 
class StudentsListView(View):
    def get(self, request, pk):
        teacher = request.user
        students_list = Enrollment.objects.filter(course=pk)
        print(students_list) 
        context = {
            'teacher': teacher,
            'students_list': students_list
        }
        return render(request, 'courses/students_list.html', context)
