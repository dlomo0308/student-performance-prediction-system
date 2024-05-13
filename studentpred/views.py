from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from .models import Student, MathPerformance, SciencePerformance, ComputerPerformance, HistoryPerformance, GeographyPerformance, PredictionHistory
from .forms import PredictionForm
import pickle, joblib
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, LabelEncoder
from django.contrib import messages
import os
from django.conf import settings
from config.settings.base import NOTEBOOK_DIR


# Define the directory path
# directory = r"C:\Users\sjr\OneDrive\Desktop\COMP SCIENCE\sjrCodes\py\DJANGO\student_performance\notebook"



# Define the file name
file_name = "svm_modell.pkl"

# Concatenate directory path and file name
# file_path = os.path.join(directory, file_name)
# file_path = os.path.join(settings.BASE_DIR, settings.NOTEBOOK_DIR, file_name)
file_path = os.path.join(NOTEBOOK_DIR, file_name)

# Create your views here.
@csrf_exempt
@login_required
def prediction(request):
    form = PredictionForm()

    if request.user.is_authenticated and hasattr(request.user, 'student'):


        if request.method == 'POST':
            form = PredictionForm(request.POST)

            if form.is_valid():
                # Retrieve student's existing data from the database
                student_data = Student.objects.filter(user=request.user).values('Mother_Education', 'sex', 'Father_Education').first()

                # Retrieve selected subject from the form
                subject = form.cleaned_data['subject']

                # Retrive slected Student from the Database
                # student = Student.objects.filter(student_id=request.user)

                # if student:
                    # Check if the user has already made a prediction for this subject
                if PredictionHistory.objects.filter(student=request.user.student, subject=subject).exists():
                    context = {'already_done': f"You have already made a prediction for {subject}.", 'form':form}
                    return render(request, 'pages/prediction.html', context)
                # else:
                #     messages.error(request, 'Student not registered')

                # Retrieve subject-specific data based on the selected subject
                if subject == 'maths':
                    subject_data = MathPerformance.objects.filter(student=request.user.student).values('extra_lessons', 'failures', 'absences', 'G1', 'G2').first()
                elif subject == 'science':
                    subject_data = SciencePerformance.objects.filter(student=request.user.student).values('extra_lessons', 'failures', 'absences', 'G1', 'G2').first()
                elif subject == 'computer':
                    subject_data = ComputerPerformance.objects.filter(student=request.user.student).values('extra_lessons', 'failures', 'absences', 'G1', 'G2').first()
                elif subject == 'history':
                    subject_data = HistoryPerformance.objects.filter(student=request.user.student).values('extra_lessons', 'failures', 'absences', 'G1', 'G2').first()
                elif subject == 'geo':
                    subject_data = GeographyPerformance.objects.filter(student=request.user.student).values('extra_lessons', 'failures', 'absences', 'G1', 'G2').first()
                else:
                    messages.error(request, "There is an error!!!")
                # Add more elif conditions for other subjects if needed

                if not student_data:
                    messages.error(request, "Student Data not found.")
                elif not subject_data:
                    messages.error(request, "Subject Data not found.")

                if student_data and subject_data:
                    # Retrieve the prediction form data
                    travel_time = form.cleaned_data['travel_time']
                    free_time = form.cleaned_data['free_time']
                    study_time = form.cleaned_data['study_time']
                    internet = form.cleaned_data['internet']
                    romantic = form.cleaned_data['romantic']
                    fam_rel = form.cleaned_data['fam_rel']
                    health_status = form.cleaned_data['health_status']

                    # Prepare data for prediction
                    prediction_input = pd.DataFrame({
                        'sex': student_data['sex'],
                        'failures': subject_data['failures'],
                        'extra_lessons': subject_data['extra_lessons'],
                        'internet': internet,
                        'romantic': romantic,
                        'absences': subject_data['absences'],
                        'G1': subject_data['G1'],
                        'G2': subject_data['G2'],
                        'M_edu': student_data['Mother_Education'],
                        'F_edu': student_data['Father_Education'],
                        'fam_rel': fam_rel,
                        'free_time': free_time,
                        'health_status': health_status,
                        'travel_time': travel_time,
                        'study_time': study_time
                    }, index=[0])
                    prediction_input.columns = ['sex', 'failures', 'extra_lessons', 'internet', 'romantic', 'absences', 'G1', 'G2', 'M_edu', 'F_edu', 'fam_rel', 'free_time', 'health_status', 'travel_time', 'study_time']

                    # Load the trained ML model from the pickle file
                    with open(file_path, 'rb') as file:
                        ml_model = joblib.load(file)

                    encoded_column_names = ['failures', 'absences', 'G1', 'G2', 'sex_M', 'extra_lessons_yes', 'internet_yes', 'romantic_yes', 'M_edu_None', 'M_edu_Primary', 'M_edu_Secondary', 'F_edu_None', 'F_edu_Primary', 'F_edu_Secondary', 'fam_rel_Excellent', 'fam_rel_Fair', 'free_time_Low', 'free_time_Moderate', 'free_time_Very High', 'free_time_Very Low', 'health_status_Fair', 'health_status_Good', 'health_status_Very Bad', 'health_status_Very Good', 'travel_time_30-60', 'travel_time_<15', 'travel_time_Above 60', 'study_time_5-10', 'study_time_<2hrs', 'study_time_Above 10']

                    # Ensure the prediction input DataFrame has the same columns as the encoded DataFrame
                    prediction_input = prediction_input.reindex(columns=encoded_column_names, fill_value=0)

                    # Make prediction
                    predicted_grade = ml_model.predict(prediction_input)

                    if predicted_grade is not None:
                        # Save the prediction result and form data to the database
                        prediction_history = PredictionHistory(
                            student=request.user.student,
                            subject=subject,
                            travel_time=travel_time,
                            free_time=free_time,
                            study_time=study_time,
                            internet=internet,
                            romantic=romantic,
                            fam_rel=fam_rel,
                            health_status=health_status,
                            prediction_result=predicted_grade[0]  # Assuming`prediction_result` is a single value
                        )
                        prediction_history.save()

                        # Store the prediction data in the session
                        request.session['prediction_data'] = {
                            'form_data': {
                                'subject': subject,
                                'travel_time': travel_time,
                                'free_time': free_time,
                                'study_time': study_time,
                                'internet': internet,
                                'romantic': romantic,
                                'fam_rel': fam_rel,
                                'health_status': health_status,
                            },
                            'prediction_result': predicted_grade.tolist()  # Convert ndarray to list
                        }

                        # Use the predicted_grade value
                        messages.success(request, 'Prediction Was Successful')
                        # context = {'predicted_grade': predicted_grade}
                        return redirect('prediction_results')
                        # return render(request, 'pages/prediction_results.html', context)

                    else:
                        # Handle the case when predicted_grade is None
                        messages.error(request, 'Failed to perform prediction')
                        return redirect('prediction')  # Redirect back to the prediction page

            else:
                messages.error(request, "Invalid Form")

        context = {'form': form}
        return render(request, 'pages/prediction.html', context)
    
    else:
        # If the user is not authenticated or is not a student, display an error message
        messages.error(request, "You need to be registered as a student to perform predictions.")
        context = {'form': form}
        return render(request, 'pages/prediction.html', context)
    


# my academic data view
@login_required
def my_previous_data(request):
    # Retrieve the math performance data for the current student
    math_data = MathPerformance.objects.filter(student__user=request.user).first()
    # Retrieve the science performance data for the current student
    science_data = SciencePerformance.objects.filter(student__user=request.user).first()
    # Retrieve the computer performance data for the current student
    computer_data = ComputerPerformance.objects.filter(student__user=request.user).first()
    # Retrieve the history performance data for the current student
    history_data = HistoryPerformance.objects.filter(student__user=request.user).first()
    # Retrieve the geo performance data for the current student
    geo_data = GeographyPerformance.objects.filter(student__user=request.user).first()

    context = {
        'math_data': math_data,
        'science_data': science_data,
        'computer_data': computer_data,
        'history_data': history_data,
        'geo_data': geo_data
    }
    return render(request, 'pages/previous_data.html', context)


def view_history(request):
    context = {}  # Initialize the context dictionary
    no_prediction_history = False
    if request.user.is_authenticated and hasattr(request.user, 'student'):
        student = request.user.student
        history = PredictionHistory.objects.filter(student=student).order_by('prediction_date')
        context = {'history':history}

        if not history:
            no_prediction_history = True
    else:
        no_prediction_history = True

    context['no_prediction_history'] = no_prediction_history
    return render(request, 'pages/history.html', context)


        # return render(request, 'pages/history.html', context)
    # else:
    #     error_message = 'You are not registered as a student, meaning you dont have any history.'
    #     # Return a JSON response containing the error message
    #     return JsonResponse({'error_message': error_message})

def prediction_results(request):
    prediction_data = request.session.get('prediction_data')
    # Initialize predicted_grade as None
    predicted_grade = None
    if prediction_data:
        predicted_grade = prediction_data.get('prediction_result')
        if predicted_grade:
            predicted_grade = predicted_grade[0]
    context = {'prediction_data': prediction_data, 'predicted_grade':predicted_grade}

    # If no prediction data is available, add a message
    if not prediction_data:
        messages.warning(request, 'No prediction has been made yet.')

    return render(request, 'pages/prediction_results.html', context)

