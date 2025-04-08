from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.student_id:
            year = timezone.now().year % 100
            prefix = f"STU{year}"
            last_id = Student.objects.filter(student_id__startswith=prefix).order_by('-student_id').values_list('student_id', flat=True).first()
            next_num = int(last_id[-4:]) + 1 if last_id else 1
            self.student_id = f"{prefix}{next_num:04d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"
    
    @property
    def name(self):
        return self.user.get_full_name()

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    faculty_id = models.CharField(max_length=20, unique=True, blank=True)
    department = models.CharField(max_length=100, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.faculty_id:
            year = timezone.now().year % 100 
            prefix = f"FAC{year}"
            last_id = Faculty.objects.filter(faculty_id__startswith=prefix).order_by('-faculty_id').values_list('faculty_id', flat=True).first()
            next_num = int(last_id[-4:]) + 1 if last_id else 1
            self.faculty_id = f"{prefix}{next_num:04d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.faculty_id})"
    
    @property
    def name(self):
        return self.user.get_full_name()