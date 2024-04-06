from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Student

# Create your views here.
@csrf_exempt
@login_required
def prediction(request):
     
    return render(request, 'pages/prediction.html')


# my academic data view
@login_required
def my_previous_data(request):
    # Get the current user
    user = request.user

    # Check if the user is authenticated
    student_data = Student.objects.filter(user=request.user)
    context = {'student_data': student_data}
    return render(request, 'pages/previous_data.html', context)
    

def view_history(request):
    return render(request, 'pages/history.html')
