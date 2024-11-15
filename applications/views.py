from django.shortcuts import render, redirect
from .forms import PersonalDetailsForm, LoanDetailsForm, DocumentUploadForm, JobDetailsForm
from .models import Application, ApplicationTracker,PersonalDetails, JobDetails, LoanDetails, DocumentUpload
from django.contrib.auth.decorators import login_required

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
            # Final submission: change status to 'submitted'
            application.status = 'submitted'
            application.save()
            return redirect('applications:application_complete')

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
                return redirect('applications:application_complete')

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

    # Render the application form with the current stage and form
    return render(request, 'application_form.html', {'form': form, 'stage': stage, 'application': application})

# Application completion view
@login_required
def application_complete_view(request):
    return render(request, 'application_complete.html')

# Enquiry form view
def enquiry_view(request):
    if request.method == 'POST':
        # Handle enquiry form submission
        pass
    return render(request, 'enquiry.html')

# FAQs view
def faqs_view(request):
    return render(request, 'faqs.html')