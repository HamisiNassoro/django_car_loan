from django import forms
from .models import Application, PersonalDetails, LoanDetails, DocumentUpload

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = '__all__'

class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = PersonalDetails
        fields = '__all__'

class LoanDetailsForm(forms.ModelForm):
    class Meta:
        model = LoanDetails
        fields = '__all__'

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = DocumentUpload
        fields = '__all__'