from django.contrib import admin
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

admin.site.register(Student, StudentAdmin)