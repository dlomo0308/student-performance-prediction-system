from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from .models import Student
from .utils import generate_student_number  # Import the generate_student_number function

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'student_name', 'address', 'extra_lessons', 'failures', 'absences', 'G1', 'G2')

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        # Generate student number and set it as the initial value for the student_id field
        initial['student_id'] = generate_student_number()  # Use the generate_student_number function

        # Add initial data for other fields
        initial['name'] = ''  # Add initial data for the name field
        initial['failures'] = 0  # Add initial data for the failures field
        initial['absences'] = 0  # Add initial data for the absences field
        initial['G1'] = 0  # Add initial data for the G1 field
        initial['G2'] = 0  # Add initial data for the G2 field
        return initial
    
    # readonly_fields = ('student_id',)
    
    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         return self.readonly_fields
    #     return self.readonly_fields

admin.site.register(Student, StudentAdmin)