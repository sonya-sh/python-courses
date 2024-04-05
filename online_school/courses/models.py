from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Course(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    teacher = models.ManyToManyField(CustomUser) # создается отдельная таблица в бд для ManyToMany поля
    
    def __str__(self):
        return self.name
    

class Lesson(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    content = models.TextField()
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='lessons') # many(lessons)->one(course)
    #course.lesson_set.all() - получить все уроки курса (обратное отношение, тк в модели Course нет поля lessons)
    #либо изменить related_name='lessons' чтобы можно было получить то же самое через course.lessons.all()

    def __str__(self):
        return self.name
    

class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)
    completed_lessons = models.ManyToManyField(Lesson, blank=True) # создается отдельная таблица в бд для ManyToMany поля

    def __str__(self):
        return f"{self.course} - {self.student}"
    
    def mark_lesson_as_completed(self, lesson):
        self.completed_lessons.add(lesson)

    def mark_lesson_as_not_completed(self, lesson):
        self.completed_lessons.remove(lesson)

    def get_completion_percentage(self):
        total_lessons = self.course.lessons.count() 
        completed_lessons = self.completed_lessons.count()
        if total_lessons == 0:
            return 0
        return (completed_lessons / total_lessons) * 100
