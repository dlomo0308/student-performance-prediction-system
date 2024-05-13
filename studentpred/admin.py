from typing import Any
from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.http import HttpRequest
from .models import Student, MathPerformance, SciencePerformance, ComputerPerformance, HistoryPerformance, GeographyPerformance, PredictionHistory
from .utils import generate_student_number  # Import the generate_student_number function

User = get_user_model()

class StudentAdminForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter existing students from the user choices
        existing_students = Student.objects.all().values_list('user_id', flat=True)
        self.fields['user'].queryset = User.objects.exclude(pk__in=existing_students)



class StudentAdmin(admin.ModelAdmin):
    form = StudentAdminForm
    list_display = ('student_id', 'student_name', 'address')

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        # Generate student number and set it as the initial value for the student_id field
        initial['student_id'] = generate_student_number()  # Use the generate_student_number function
        # Add initial data for other fields
        initial['name'] = ''  # Add initial data for the name field
        return initial
admin.site.register(Student, StudentAdmin)

class MathsAdmin(admin.ModelAdmin):
    list_display = ('student', 'extra_lessons', 'failures', 'absences', 'G1', 'G2')
admin.site.register(MathPerformance, MathsAdmin)

class ScienceAdmin(admin.ModelAdmin):
    list_display = ('student', 'extra_lessons', 'failures', 'absences', 'G1', 'G2')
admin.site.register(SciencePerformance, ScienceAdmin)

class ComputerAdmin(admin.ModelAdmin):
    list_display = ('student', 'extra_lessons', 'failures', 'absences', 'G1', 'G2')
admin.site.register(ComputerPerformance, ComputerAdmin)

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('student', 'extra_lessons', 'failures', 'absences', 'G1', 'G2')
admin.site.register(HistoryPerformance, HistoryAdmin)

class GeographyAdmin(admin.ModelAdmin):
    list_display = ('student', 'extra_lessons', 'failures', 'absences', 'G1', 'G2')
admin.site.register(GeographyPerformance, GeographyAdmin)

class PredictionHistoryAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'prediction_date', 'prediction_result')
admin.site.register(PredictionHistory, PredictionHistoryAdmin)
