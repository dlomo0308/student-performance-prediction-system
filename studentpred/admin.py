from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from .models import Student, MathPerformance, SciencePerformance, ComputerPerformance
from .utils import generate_student_number  # Import the generate_student_number function

class StudentAdmin(admin.ModelAdmin):
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
