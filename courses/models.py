from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=200)
    offered_by = models.ForeignKey('accounts.Faculty', on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.course_code}: {self.course_name}"

class Registration(models.Model):
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, related_name='registrations')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['student', 'course']
    
    def __str__(self):
        return f"{self.student} registered for {self.course}"
    
    def clean(self):
        if self.student_id is None:
            return
        active_registrations = Registration.objects.filter(student=self.student)
        if active_registrations.count() >= 2 and not active_registrations.filter(course=self.course).exists():
            raise ValidationError("Students can register for a maximum of 2 courses.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)