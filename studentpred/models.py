from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from django.conf import settings

# COMMON CHOICES FOR ALL SUBJECTS
SEX_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]

EXTRA_LESSONS_CHOICES = [
    ('yes', 'YES'),
    ('no', 'NO'),
]

ADDRESS_CHOICES = [
    ('SR', 'School Residents'),
    ('NR', 'Non Residential'),
]

EDU_CHOICES = [
    ('None', 'None'),
    ('Primary', 'Primary Education'),
    ('Secondary', 'Secondary Education'),
    ('Higher', 'Higher Education'),
]

JOB_CHOICES = [
    ('teacher', 'Teacher'),
    ('health', 'Healthcare Related'),
    ('services', 'Civil Services'),
    ('at_home', 'At Home'),
    ('other', 'Other'),
]

# student model
class Student(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, primary_key=True)
    student_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=10)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    address = models.CharField(max_length=3, choices=ADDRESS_CHOICES) # no longer in dataframe but we will record it
    # famsize = models.CharField(max_length=3, choices=FAMSIZE_CHOICES)
    Mother_Education = models.IntegerField(choices=EDU_CHOICES)
    Father_Education = models.IntegerField(choices=EDU_CHOICES)
    Mother_job = models.CharField(max_length=20, choices=JOB_CHOICES)
    Father_job = models.CharField(max_length=20, choices=JOB_CHOICES)

    def __str__(self):
        return self.user.username
    
class MathPerformance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    extra_lessons = models.CharField(max_length=3, choices=EXTRA_LESSONS_CHOICES)
    failures = models.PositiveIntegerField(validators=[MaxValueValidator(4)])
    absences = models.PositiveIntegerField(validators=[MaxValueValidator(90)])
    G1 = models.PositiveIntegerField(validators=[MaxValueValidator(20)])
    G2 = models.PositiveIntegerField(validators=[MaxValueValidator(20)])
    
class SciencePerformance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    extra_lessons = models.CharField(max_length=3, choices=EXTRA_LESSONS_CHOICES)
    failures = models.PositiveIntegerField(validators=[MaxValueValidator(4)])
    absences = models.PositiveIntegerField(validators=[MaxValueValidator(90)])
    G1 = models.PositiveIntegerField(validators=[MaxValueValidator(20)])
    G2 = models.PositiveIntegerField(validators=[MaxValueValidator(20)])
    
class ComputerPerformance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    extra_lessons = models.CharField(max_length=3, choices=EXTRA_LESSONS_CHOICES)
    failures = models.PositiveIntegerField(validators=[MaxValueValidator(4)])
    absences = models.PositiveIntegerField(validators=[MaxValueValidator(90)])
    G1 = models.PositiveIntegerField(validators=[MaxValueValidator(20)])
    G2 = models.PositiveIntegerField(validators=[MaxValueValidator(20)])

# Model to save the prediction history
class PredictionHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    travel_time = models.CharField(max_length=255)
    free_time = models.CharField(max_length=255)
    study_time = models.CharField(max_length=255)
    internet = models.CharField(max_length=255)
    romantic = models.CharField(max_length=255)
    fam_rel = models.CharField(max_length=255)
    health_status = models.CharField(max_length=255)
    prediction_result = models.DecimalField(max_digits=5, decimal_places=2)
    prediction_date = models.DateTimeField(auto_now_add=True)
    


