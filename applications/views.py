from django.shortcuts import render, redirect
from .forms import PersonalDetailsForm, LoanDetailsForm, DocumentUploadForm, JobDetailsForm
from .models import Application, ApplicationTracker
from django.contrib.auth.decorators import login_required

# Create your views here.

# Home page view
def home(request):
    return render(request, 'home.html')

# Multi-step form for application
@login_required
def application_form(request):
    # Retrieve or create an active application for the user
    application = Application.objects.filter(user=request.user, status='pending').order_by('-created_at').first()

    # If no pending application exists, create a new one
    if not application:
        application = Application.objects.create(user=request.user, status='pending')
    
    stage = request.POST.get('stage', '1')  # Default to stage 1 if no stage is specified

    if request.method == 'POST':
        if stage == '1':
            form = PersonalDetailsForm(request.POST)
            if form.is_valid():
                personal_details = form.save(commit=False)
                personal_details.application = application
                personal_details.save()
                return redirect('applications:application_form')  # Move to next stage

        elif stage == '2':
            form =  JobDetailsForm(request.POST)
            if form.is_valid():
                job_details = form.save(commit=False)
                job_details.application = application
                job_details.save()
                return redirect('applications:application_form')  # Move to next stage

        elif stage == '3':
            form = LoanDetailsForm(request.POST)
            if form.is_valid():
                loan_details = form.save(commit=False)
                loan_details.application = application
                loan_details.save()
                return redirect('applications:application_form')  # Move to next stage

        elif stage == '4':
            form = DocumentUploadForm(request.POST, request.FILES)
            if form.is_valid():
                document_upload = form.save(commit=False)
                document_upload.application = application
                document_upload.save()
                return redirect('applications:application_complete')  # Final step after upload
    else:
        # Display the form for the current stage
        if stage == '1':
            form = PersonalDetailsForm()
        elif stage == '2':
            form = JobDetailsForm()
        elif stage == '3':
            form = LoanDetailsForm()
        elif stage == '4':
            form = DocumentUploadForm()

    # Render the form with the current stage
    return render(request, 'application_form.html', {'form': form, 'stage': stage})

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