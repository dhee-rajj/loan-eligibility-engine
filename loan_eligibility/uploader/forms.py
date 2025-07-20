from django import forms

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField(label='Upload CSV File')
