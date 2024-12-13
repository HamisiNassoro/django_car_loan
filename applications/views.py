from django.shortcuts import render, redirect
from .forms import PersonalDetailsForm, LoanDetailsForm, DocumentUploadForm, JobDetailsForm
from .models import Application, ApplicationTracker,PersonalDetails, JobDetails, LoanDetails, DocumentUpload, Invoice
from django.contrib.auth.decorators import login_required
from .utils import generate_invoice_pdf
from django.shortcuts import get_object_or_404
from django.http import FileResponse
import logging

logger = logging.getLogger(__name__)

# Create your views here.

# Home page view
def home(request):
    return render(request, 'home.html')

# Multi-step application form view
@login_required
def application_form(request):
    # Retrieve the latest pending application for the user, or create a new one
    application, created = Application.objects.get_or_create(
        user=request.user,
        status='pending',
    )

    # Determine the current stage from POST data, defaulting to stage 1
    stage = request.POST.get('stage', '1')

    if request.method == 'POST':
        # Handle stage progression
        if request.POST.get('next'):
            stage = str(int(stage) + 1)
        elif request.POST.get('prev'):
            stage = str(int(stage) - 1)
        elif request.POST.get('submit'):
            # Final submission: update status and generate invoice
            application.status = 'submitted'
            application.save()

            # Create an invoice if not already created
            # Create the invoice if it doesn't exist
            invoice, created = Invoice.objects.get_or_create(application=application, defaults={'amount_due': 500})

            # Redirect to application complete page with the application ID
            return redirect('applications:application_complete', application_id=application.id)

        # Handle form submission for each stage
        if stage == '1':
            personal_details_instance = PersonalDetails.objects.filter(application=application).first()
            form = PersonalDetailsForm(request.POST, instance=personal_details_instance)
            if form.is_valid():
                personal_details = form.save(commit=False)
                personal_details.application = application
                personal_details.save()
                stage = '2'  # Move to next stage after saving

        elif stage == '2':
            if not hasattr(application, 'personal_details'):
                return redirect('applications:application_form')
            job_details_instance = JobDetails.objects.filter(personal_details=application.personal_details).first()
            form = JobDetailsForm(request.POST, instance=job_details_instance)
            if form.is_valid():
                job_details = form.save(commit=False)
                job_details.personal_details = application.personal_details
                job_details.save()
                stage = '3'  # Move to next stage after saving

        elif stage == '3':
            loan_details_instance = LoanDetails.objects.filter(application=application).first()
            form = LoanDetailsForm(request.POST, instance=loan_details_instance)
            if form.is_valid():
                loan_details = form.save(commit=False)
                loan_details.application = application
                loan_details.save()
                stage = '4'  # Move to next stage after saving

        elif stage == '4':
            form = DocumentUploadForm(request.POST, request.FILES)
            if form.is_valid():
                document_upload = form.save(commit=False)
                document_upload.application = application
                document_upload.save()
                stage = '5'  # Move to final stage after saving

    else:
        # Load the correct form for the current stage
        if stage == '1':
            form = PersonalDetailsForm(instance=PersonalDetails.objects.filter(application=application).first())
        elif stage == '2':
            if not hasattr(application, 'personal_details'):
                return redirect('applications:application_form')
            form = JobDetailsForm(instance=JobDetails.objects.filter(personal_details=application.personal_details).first())
        elif stage == '3':
            form = LoanDetailsForm(instance=LoanDetails.objects.filter(application=application).first())
        elif stage == '4':
            form = DocumentUploadForm()
        elif stage == '5':
            # No form needed for stage 5
            form = None

    # Render the application form with the current stage and form
    return render(request, 'application_form.html', {'form': form, 'stage': stage, 'application': application})

# Application completion view
# @login_required
def application_complete_view(request, application_id):
    # Retrieve the application using the provided ID
    application = get_object_or_404(Application, id=application_id, user=request.user)

    # Render the completion template
    return render(request, 'application_complete.html', {'application': application})



# Enquiry form view
def enquiry_view(request):
    if request.method == 'POST':
        # Handle enquiry form submission
        pass
    return render(request, 'enquiry.html')

# FAQs view
def faqs_view(request):
    return render(request, 'faqs.html')

def create_application(request):
    if request.method == "POST":
        # Create the application
        application = Application.objects.create(user=request.user, status="pending")
        print(f"Created application with ID: {application.id}")  # Debugging line

        # Example fee
        amount_due = 500  
        # Create the invoice
        invoice = Invoice.objects.create(application=application, amount_due=amount_due)
        print(f"Invoice created with ID: {invoice.id}")  # Debugging line

        # Redirect to the invoice download page
        return redirect("applications:download_invoice", application_id=application.id)
    
    return render(request, "application_form.html")



# Application completion view
@login_required
def application_complete_view(request):
    application = Application.objects.filter(user=request.user, status='submitted').last()
    if not application:
        return redirect("applications:application_form")

    # Ensure invoice exists
    invoice, created = Invoice.objects.get_or_create(application=application, defaults={"amount_due": 500})
    if created:
        print(f"Invoice created for application ID: {application.id}")

    return redirect("applications:download_invoice", application_id=application.id)



# Download Invoice View
def download_invoice(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    
    # Try to get the invoice or create it if it doesn't exist
    invoice, created = Invoice.objects.get_or_create(application=application, defaults={'amount_due': 500})

    # Check if the invoice was created successfully
    if not created:
        print(f"Invoice found for application {application_id}")

    buffer = generate_invoice_pdf(application, invoice.amount_due)

    # Serve the PDF as a response
    response = FileResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=invoice_{application.tracking_number}.pdf"
    return response
