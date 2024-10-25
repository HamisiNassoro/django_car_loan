from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.utils import timezone

# Tracks the last used application number for generating unique tracking numbers
class ApplicationTracker(models.Model):
    last_number = models.PositiveIntegerField(default=0)  # Holds the last used tracking number

    def __str__(self):
        return f"Last Application Number: {self.last_number}"

# Main Application model to store each loan application
class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links application to a specific user
    tracking_number = models.CharField(max_length=20, unique=True, editable=False)  # Unique ID for each application
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Default status of 'pending'
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically sets timestamp when application is created

    def save(self, *args, **kwargs):
        # Auto-generates tracking number if it doesn't exist
        if not self.tracking_number:
            tracker, _ = ApplicationTracker.objects.get_or_create(id=1)
            tracker.last_number += 1
            tracker.save()
            # Generates tracking number in the format "APP-001"
            self.tracking_number = f"APP-{tracker.last_number:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tracking_number} - {self.user.username}"

# Stores personal details for each application
class PersonalDetails(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name="personal_details")  # One-to-one link with Application
    title = models.CharField(max_length=5, choices=[('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Miss', 'Miss'), ('Ms', 'Ms'), ('Dr', 'Dr'), ('Prof', 'Prof')], default='Mr')  # Default title as 'Mr'
    surname = models.CharField(max_length=100)  # Applicant's last name
    other_names = models.CharField(max_length=100)  # Applicant's other names
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], default='M')  # Default gender as 'Male'
    date_of_birth = models.DateField()  # Applicant's date of birth
    national_id = models.CharField(max_length=20, unique=True)  # National ID number
    spouse_id = models.CharField(max_length=20, blank=True, null=True)  # Spouse's ID, optional
    ministry_department = models.CharField(max_length=100)  # Ministry or department where the applicant works
    job_group_scale = models.CharField(max_length=50)  # Job group or scale of the applicant
    current_net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Default salary of 0.00

    def __str__(self):
        return f"{self.surname} {self.other_names}"

# Stores loan details for each application
class LoanDetails(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name="loan_details")  # One-to-one link with Application
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0.00)  # Default loan amount of 0.00
    repayment_period = models.PositiveIntegerField(default=12)  # Default repayment period of 12 months
    vehicle_make = models.CharField(max_length=50, default="Unknown")  # Default make of 'Unknown'
    vehicle_model = models.CharField(max_length=50, default="Unknown")  # Default model of 'Unknown'
    vehicle_year = models.PositiveIntegerField(default=2000)  # Default year as 2000
    vehicle_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # Default cost of 0.00
    insurance_premium = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Optional insurance premium for the loan
    total_loan_required = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # Default total loan required of 0.00

    def __str__(self):
        return f"Loan for {self.application.tracking_number}"

# Manages document uploads related to each application
class DocumentUpload(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('national_id', 'National ID'),
        ('payslip', 'Payslip'),
        ('spouse_id', 'Spouse ID'),
        ('next_of_kin_id', 'Next of Kin ID'),
        ('birth_certificate', 'Birth Certificate'),
        ('ncpwd_card', 'NCPWD Card'),
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

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="documents")  # Links to Application model
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)  # Type of document being uploaded
    document = models.FileField(upload_to='documents/', validators=[
        FileExtensionValidator(allowed_extensions=['pdf', 'jpeg', 'jpg'])
    ])  # File field to store the document with file extension validation
    uploaded_at = models.DateTimeField(default=timezone.now)  # Timestamp for document upload
    is_validated = models.BooleanField(default=False)  # Document validation status (approved/rejected)

    def __str__(self):
        return f"{self.document_type} for {self.application.tracking_number}"
