from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.

from django.db import models

class ApplicationTracker(models.Model):
    last_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Last Application Number: {self.last_number}"

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=20, unique=True, editable=False)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Generate the tracking number
        if not self.tracking_number:  # Only create if it hasn't been set yet
            tracker, created = ApplicationTracker.objects.get_or_create(id=1)  # Use a single tracker
            tracker.last_number += 1
            tracker.save()
            self.tracking_number = f"APP-{tracker.last_number:03d}"  # Format as APP-001, APP-002, etc.
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Application {self.tracking_number} - {self.user.username}"

class PersonalDetails(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=20)
    spouse_id = models.CharField(max_length=20, blank=True, null=True)
    ministry_department = models.CharField(max_length=100)
    employment_details = models.CharField(max_length=100)

    def __str__(self):
        return f"Personal Details for {self.application.tracking_number}"

class LoanDetails(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    repayment_period = models.PositiveIntegerField()
    vehicle_make = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    vehicle_year = models.PositiveIntegerField()

    def __str__(self):
        return f"Loan Details for {self.application.tracking_number}"

class DocumentUpload(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50, choices=[
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
    ])
    document = models.FileField(upload_to='documents/', validators=[
        FileExtensionValidator(allowed_extensions=['pdf', 'jpeg', 'jpg'])
    ])
    is_validated = models.BooleanField(default=False)  # New field for document validation status

    def __str__(self):
        return f"Document {self.document_type} for {self.application.tracking_number}"
