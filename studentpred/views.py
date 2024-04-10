from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Student
from .forms import PredictionForm
import pickle, joblib
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

# Create your views here.
@csrf_exempt
@login_required
def prediction(request):
    form = PredictionForm()
    if request.method == 'POST':
        form = PredictionForm(request.POST)

        
        if form.is_valid():

            # Define the mapping between form field names and model field names
            field_mapping = {
                'travel_time': 'travel_time',
                'free_time': 'free_time',
                'study_time': 'study_time',
                'internet': 'internet',
                'romantic': 'romantic',
                'fam_rel': 'fam_rel',
            }

        
            # Retrieve student's existing data from the database
            student_data = Student.objects.filter(user=request.user).values('Mother_Education', 'extra_lessons', 'sex', 'Father_Education', 'failures', 'absences', 'G1', 'G2').first()

            # Define the mapping between DataFrame column names and model field names
            column_mapping = {
                'M_edu': 'Mother_Education',
                'F_edu': 'Father_Education',
                'paid': 'extra_lessons',
                # Add other mappings if needed
            }

            if student_data:
                # Retrieve the prediction form data
                travel_time = form.cleaned_data['travel_time']
                free_time = form.cleaned_data['free_time']
                study_time = form.cleaned_data['study_time']
                internet = form.cleaned_data['internet']
                romantic = form.cleaned_data['romantic']
                fam_rel = form.cleaned_data['fam_rel']
                health_status = form.cleaned_data['health_status']
                
                # Prepare data for prediction
                prediction_input = pd.DataFrame([[student_data[column_mapping['M_edu']],
                                                student_data[column_mapping['F_edu']],
                                                student_data[column_mapping['paid']],
                                                student_data['sex'],
                                                student_data['failures'],
                                                student_data['absences'],
                                                student_data['G1'],
                                                student_data['G2'],
                                                travel_time,
                                                free_time,
                                                study_time,
                                                internet,
                                                romantic,
                                                fam_rel,
                                                health_status]],
                                                columns=['sex', 'failures', 'paid', 'internet', 'romantic', 'absences', 'G1', 'G2', 'M_edu', 'F_edu',
                                                        'fam_rel', 'free_time', 'health_status', 'travel_time', 'study_time'])

                # Apply one-hot encoding
                # categorical_variables = ['M_edu', 'F_edu', 'travel_time', 'free_time', 'study_time', 'internet', 'romantic', 'fam_rel']
                # prediction_input_encoded = pd.get_dummies(prediction_input, columns=categorical_variables, drop_first=True, dtype=int)

                # Load the trained ML model from the pickle file
                with open(r"C:\Users\sjr\OneDrive\Desktop\COMP SCIENCE\sjrCodes\py\DJANGO\student_performance\notebook\svm_model.sav", 'rb') as file:
                    ml_model = joblib.load(file)

                # ml_model = joblib.load('svm_model.sav')

                # Create an instance of the OrdinalEncoder
                encoder = OrdinalEncoder()

                # Perform ordinal encoding on the prediction input data
                prediction_input_encoded = encoder.fit_transform(prediction_input)
                    
                # Make prediction
                predicted_grade = ml_model.predict(prediction_input_encoded)

                # Convert the predicted_grade to a scalar value (if necessary)
                predicted_grade = predicted_grade[0] if len(predicted_grade) > 0 else None
                            
            

        context = {'form': form, 'prediction_grade':predicted_grade}
        # context = {'predicted_grade': predicted_grade}

        return render(request, 'pages/prediction.html', context)
    else:
        context = {'form': form}
        return render(request, 'pages/prediction.html',context)
     
    # return render(request, 'pages/prediction.html')


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
