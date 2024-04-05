from django import forms
from .models import Course, Lesson
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CourseCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = CustomUser.objects.filter(customuser_group__name='Teachers')

    class Meta:
        model = Course
        fields = ['name', 'description', 'start_date', 'end_date', 'is_active', 'teacher']
        widgets = {
            'teacher': forms.CheckboxSelectMultiple(),
        }

class CourseEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = CustomUser.objects.filter(customuser_group__name='Teachers')

    class Meta:
        model = Course
        fields = ('name', 'description', 'start_date', 'end_date', 'is_active', 'teacher')
        widgets = {
            'teacher': forms.CheckboxSelectMultiple(),
        }

class SubscribeForm(forms.Form):
    pass

class LessonDoneForm(forms.Form):
    pass

class LessonCreationForm(forms.ModelForm):
    
    class Meta:
        model = Lesson
        fields = ('name', 'description', 'content')
