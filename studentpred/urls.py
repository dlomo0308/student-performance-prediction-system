from django.urls import path
from .views import prediction, view_history, my_previous_data

app_name = 'studentpred'

urlpatterns = [
    # path('studentpred', st),
    path('prediction/', prediction, name='prediction'),
    path('myhistory/', view_history, name='myhistory'),
    path('mydata/', my_previous_data, name='mydata'),
]
