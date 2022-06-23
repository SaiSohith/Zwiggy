from django import forms
from .models import tablebooking


class bookingtableform(forms.ModelForm):
    img = forms.ImageField(label='profileimg')
    class Meta:
        model = tablebooking
        fields = ['name', 'tableno', 'date', 'time']
        labels = ['Name', 'Table Number', 'Date', 'Time']
        widgets = {
            'date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
            'time': forms.TimeInput(format='%H:%M')
        }
