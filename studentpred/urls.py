from django.urls import path
from .views import prediction, view_history, my_previous_data, prediction_results

app_name = 'studentpred'

urlpatterns = [
    # path('studentpred', st),
    path('prediction/', prediction, name='prediction'),
    path('myhistory/', view_history, name='myhistory'),
    path('predictionresults/', prediction_results, name='predictionhistory'),
    path('mydata/', my_previous_data, name='mydata'),
]
