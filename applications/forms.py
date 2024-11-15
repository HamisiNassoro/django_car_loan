from django import forms
from .models import Application, PersonalDetails, LoanDetails, DocumentUpload, JobDetails

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = '__all__'

class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = PersonalDetails
        fields = '__all__'

class JobDetailsForm(forms.ModelForm):
    class Meta:
        model = JobDetails
        fields = '__all__'

class LoanDetailsForm(forms.ModelForm):
    class Meta:
        model = LoanDetails
        fields = '__all__'

class DocumentUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Get 'personal_details' instance to check for physical disability
        self.personal_details = kwargs.pop('personal_details', None)
        super().__init__(*args, **kwargs)

        # Define default document type choices excluding NCPWD Card
        document_type_choices = [
            ('national_id', 'National ID'),
            ('payslip', 'Payslip'),
            ('spouse_id', 'Spouse ID'),
            ('next_of_kin_id', 'Next of Kin ID'),
            ('birth_certificate', 'Birth Certificate'),
            ('appointment_letter', 'Appointment Letter'),
            ('logbook', 'Logbook'),
            ('sale_agreement', 'Sale Agreement'),
            ('pin_certificate', 'PIN Certificate'),
            ('proforma_invoice', 'Proforma Invoice'),
            ('valuation_report', 'Valuation Report'),
            ('payment_proof', 'Payment Proof'),
            ('hr_letter', 'HR Letter'),
            ('bank_statement', 'Bank Statement'),
            ('bank_details', 'Bank Details'),
        ]

        # Add 'NCPWD Card' if the applicant has a physical disability
        if self.personal_details and self.personal_details.physical_disability:
            document_type_choices.append(('ncpwd_card', 'NCPWD Card'))

        # Update field choices
        self.fields['document_type'].choices = document_type_choices

    class Meta:
        model = DocumentUpload
        fields = ['document_type', 'document']
