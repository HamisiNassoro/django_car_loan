from django import forms
from .models import PersonalDetails, LoanDetails, DocumentUpload

class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = PersonalDetails
        fields = ['name', 'national_id', 'spouse_id', 'ministry_department', 'employment_details']

class LoanDetailsForm(forms.ModelForm):
    class Meta:
        model = LoanDetails
        fields = ['loan_amount', 'repayment_period', 'vehicle_make', 'vehicle_model', 'vehicle_year']

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = DocumentUpload
        fields = ['document_type', 'document']
