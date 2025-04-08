from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Course, Registration
from .forms import CourseForm, RegistrationForm

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def create_course(request):
    if request.user.user_type != 'faculty':
        messages.error(request, "Only faculty members can create courses.")
        return redirect('course_list')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.offered_by = request.user.faculty_profile
            course.save()
            messages.success(request, f"Course '{course.course_name}' has been created successfully.")
            return redirect('faculty_dashboard')
    else:
        form = CourseForm()
    
    return render(request, 'courses/create_course.html', {'form': form})

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.user.user_type != 'faculty' or course.offered_by.user != request.user:
        messages.error(request, "You don't have permission to edit this course.")
        return redirect('course_list')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f"Course '{course.course_name}' has been updated successfully.")
            return redirect('faculty_dashboard')
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'courses/edit_course.html', {'form': form, 'course': course})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.user.user_type != 'faculty' or course.offered_by.user != request.user:
        messages.error(request, "You don't have permission to delete this course.")
        return redirect('course_list')
    
    if request.method == 'POST':
        course_name = course.course_name
        course.delete()
        messages.success(request, f"Course '{course_name}' has been deleted successfully.")
        return redirect('faculty_dashboard')
    
    return render(request, 'courses/delete_course.html', {'course': course})

@login_required
def register_for_course(request):
    if request.user.user_type != 'student':
        messages.error(request, "Only students can register for courses.")
        return redirect('course_list')
    
    student = request.user.student_profile
    registrations_count = student.registrations.count()
    
    if registrations_count >= 2:
        messages.error(request, "You have already registered for the maximum number of courses (2).")
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.student = student
            registration.save()
            messages.success(request, f"Course registered successfully")
            return redirect('student_dashboard')
    else:
        registered_courses = student.registrations.values_list('course', flat=True)
        form = RegistrationForm()
        form.fields['course'].queryset = Course.objects.exclude(id__in=registered_courses)
    
    return render(request, 'courses/register_course.html', {'form': form})