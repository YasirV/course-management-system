from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomAuthenticationForm, StudentRegistrationForm, FacultyRegistrationForm
from .models import User, Student, Faculty

def login_view(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'student':
            return redirect('student_dashboard')
        else:
            return redirect('faculty_dashboard')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == 'student':
                    return redirect('student_dashboard')
                else:
                    return redirect('faculty_dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if not hasattr(user, 'student_profile'):
                Student.objects.create(user=user)
            login(request, user)
            return redirect('student_dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/register_student.html', {'form': form})

def register_faculty(request):
    if request.method == 'POST':
        form = FacultyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            faculty = Faculty(
                user=user,
                department=form.cleaned_data.get('department', '')
            )
            faculty.save()
            login(request, user)
            return redirect('faculty_dashboard')
    else:
        form = FacultyRegistrationForm()
    return render(request, 'accounts/register_faculty.html', {'form': form})

@login_required
def student_dashboard(request):
    if request.user.user_type != 'student':
        messages.error(request, "Access denied. Student access only.")
        return redirect('login')
    
    student = request.user.student_profile
    registrations = student.registrations.all()
    
    return render(request, 'accounts/student_dashboard.html', {
        'student': student,
        'registrations': registrations
    })

@login_required
def faculty_dashboard(request):
    if request.user.user_type != 'faculty':
        messages.error(request, "Access denied. Faculty access only.")
        return redirect('login')
    
    faculty = request.user.faculty_profile
    courses = faculty.courses.all()
    
    return render(request, 'accounts/faculty_dashboard.html', {
        'faculty': faculty,
        'courses': courses
    })