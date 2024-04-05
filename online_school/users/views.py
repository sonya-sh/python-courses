from django.views import View
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, CustomUserForm, ProfileForm
from .models import Profile, CustomUser
from django.views.generic import TemplateView

    
class RegistrationView(View):

    def get(self, request):
        context = {
            'form' : RegistrationForm()
        }
        return render(request, 'registration/registration.html', context)
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
        
            user.customuser_group = form.cleaned_data['customuser_group']    
            user.save()
            user.groups.add(form.cleaned_data['customuser_group'])
            login(request, user)

            return redirect('home')
        else:
            context = {
            'form': form
        }
        return render(request, 'registration/registration.html', context)
        

class UserProfile(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        custom_user = CustomUser.objects.get(email=user.email)
        profile, created = Profile.objects.get_or_create(user=user)
        context = {
            'custom_user': custom_user,
            'profile': profile
        } 

        return render(request, 'users/profile.html', context)
    

class UserProfileEdit(View):
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get(self, request):
        user = request.user
        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user)
        custom_user = CustomUserForm(instance=user)
        profile = ProfileForm(instance=user.profile)

        context = {
            'custom_user_form': custom_user,
            'profile_form': profile,
            }
        return render(request, 'users/profile_change.html', context)
    
    def post(self, request):
        custom_user_form = CustomUserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        
        if custom_user_form.is_valid() and profile_form.is_valid():
            custom_user_form.save()
            profile_form.save()
            return redirect('profile')
            
        else:
            context = {
            'custom_user_form': custom_user_form,
            'profile_form': profile_form,
            }
            
            return render(request, 'users/profile_change.html', context)