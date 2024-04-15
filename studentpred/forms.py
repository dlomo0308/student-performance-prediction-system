from django import forms

class PredictionForm(forms.Form):
    TRAVEL_TIME_CHOICES = [
        ('<15', '<15 min.'),
        ('15-30', '15 to 30 min.'),
        ('30-60', '30 min. to 1 hour'),
        ('Above 60', '>1 hour'),
    ]

    STUDY_TIME_CHOICES = [
        ('<2hrs', '<2 hours'),
        ('2-5', '2 to 5 hours'),
        ('5-10', '5 to 10 hours'),
        ('Above 10', '>10 hours'),
    ]

    YES_NO_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    FREE_TIME_CHOICES = [
        ('Very Low', 'Very Low'),
        ('Low', 'Low'),
        ('Moderate', 'Moderate'),
        ('High', 'High'),
        ('Very High', 'Very High'),
    ]
    REL_CHOICES = [
        ('Bad', 'Bad'),
        ('Fair', 'Fair'),
        ('Excellent', 'Excellent'),
    ]

    SUB_CHOICES = [
        ('maths', 'Maths'),
        ('science', 'Science'),
        ('computer', 'Computers'),
    ]

    subject = forms.ChoiceField(label='Choose Subject', choices=SUB_CHOICES, widget=forms.Select(attrs={'class': 'form-control mb-4'}),
        required=True)
    travel_time = forms.ChoiceField(label='Home to School Travel Time', choices=TRAVEL_TIME_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}),
        required=True)
    free_time = forms.ChoiceField(label='Home to School Travel Time', choices=FREE_TIME_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}),
        required=True)
    study_time = forms.ChoiceField(label='Weekly Study Time', choices=STUDY_TIME_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}),
        required=True)
    internet = forms.ChoiceField(label='Internet Access at Home', choices=YES_NO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}),
        required=True)
    romantic = forms.ChoiceField(label='With a Romantic Relationship', choices=YES_NO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}),
        required=True)
    fam_rel = forms.ChoiceField(label='Family Relationship', choices=REL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}),
        required=True)
    health_status = forms.ChoiceField(label='Health Status', choices=REL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}),
        required=True)


