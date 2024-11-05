from django.shortcuts import render, redirect
from .forms import PersonalDetailsForm, LoanDetailsForm, DocumentUploadForm
from .models import Application, ApplicationTracker
from django.contrib.auth.decorators import login_required

# Create your views here.

# Home page view
def home(request):
    return render(request, 'home.html')

# Stage 1: Personal Information
@login_required
def personal_details_view(request):
    if request.method == 'POST':
        form = PersonalDetailsForm(request.POST)
        if form.is_valid():
            application = Application.objects.create(user=request.user)
            personal_details = form.save(commit=False)
            personal_details.application = application
            personal_details.save()
            return redirect('loan_details')  # Go to the next stage
    else:
        form = PersonalDetailsForm()
    return render(request, 'personal_details.html', {'form': form})

# Stage 2: Loan Application Details
@login_required
def loan_details_view(request):
    application = Application.objects.filter(user=request.user).last()  # Assuming latest application is active
    if request.method == 'POST':
        form = LoanDetailsForm(request.POST)
        if form.is_valid():
            loan_details = form.save(commit=False)
            loan_details.application = application
            loan_details.save()
            return redirect('document_upload')  # Go to the next stage
    else:
        form = LoanDetailsForm()
    return render(request, 'loan_details.html', {'form': form})

# Stage 3: Document Upload & Fee Payment
@login_required
def document_upload_view(request):
    application = Application.objects.filter(user=request.user).last()  # Assuming latest application is active
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document_upload = form.save(commit=False)
            document_upload.application = application
            document_upload.save()
            return redirect('application_complete')  # Final step after upload
    else:
        form = DocumentUploadForm()
    return render(request, 'document_upload.html', {'form': form})

# Application Complete
@login_required
def application_complete_view(request):
    return render(request, 'application_complete.html')

# Enquiry Form
def enquiry_view(request):
    if request.method == 'POST':
        # Logic for handling enquiry form submissions
        pass
    return render(request, 'enquiry.html')

# FAQs view
def faqs_view(request):
    return render(request, 'faqs.html')