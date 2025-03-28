from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
    faculty_student_id = models.CharField(max_length=20, unique=True)

    # Add related_name to avoid conflicts with Django's default User model
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    def __str__(self):
        return self.username


# from django.db import models

# class CourseOutcome(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()

# class ProgramOutcome(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()

# class COPOMap(models.Model):
#     co = models.ForeignKey(CourseOutcome, on_delete=models.CASCADE)
#     po = models.ForeignKey(ProgramOutcome, on_delete=models.CASCADE)
#     justification = models.TextField()
from django.db import models


class CourseOutcome(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class ProgramOutcome(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class COPOMap(models.Model):
    co = models.ForeignKey(CourseOutcome, on_delete=models.CASCADE)
    po = models.ForeignKey(ProgramOutcome, on_delete=models.CASCADE)
    alignment_level = models.CharField(max_length=10, choices=[("Strong", "Strong"), ("Moderate", "Moderate")])
    justification = models.TextField()

    def __str__(self):
        return f"{self.co.name} → {self.po.name}"

class Assessment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    co = models.ForeignKey(CourseOutcome, on_delete=models.CASCADE)
    marks_obtained = models.FloatField()
    total_marks = models.FloatField()
    assessment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.co.name}"

class POProgress(models.Model):
    po = models.ForeignKey(ProgramOutcome, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    progress_percentage = models.FloatField(default=0.0)  # Automatically updated

    def __str__(self):
        return f"{self.student.username} - {self.po.name} ({self.progress_percentage}%)"


from django.db import models
from django.utils import timezone

# models.py
from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name}"
