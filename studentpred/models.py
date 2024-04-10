from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from django.conf import settings

# student model
class Student(models.Model):
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

    # FAMSIZE_CHOICES = [
    #     ('LE3', 'Less or equal to 3'),
    #     ('GT3', 'Greater than 3'),
    # ]

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
    extra_lessons = models.CharField(max_length=3, choices=EXTRA_LESSONS_CHOICES, default='NO')
    failures = models.PositiveIntegerField(validators=[MaxValueValidator(4)])
    absences = models.PositiveIntegerField(validators=[MaxValueValidator(90)])
    G1 = models.PositiveIntegerField(validators=[MaxValueValidator(20)])
    G2 = models.PositiveIntegerField(validators=[MaxValueValidator(20)])

    def __str__(self):
        return self.user.username
    


