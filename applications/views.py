# applications/views.py
from rest_framework import viewsets
from .models import Application, PersonalDetails, LoanDetails, DocumentUpload
from .serializers import ApplicationSerializer, PersonalDetailsSerializer, LoanDetailsSerializer, DocumentUploadSerializer

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

class PersonalDetailsViewSet(viewsets.ModelViewSet):
    queryset = PersonalDetails.objects.all()
    serializer_class = PersonalDetailsSerializer

class LoanDetailsViewSet(viewsets.ModelViewSet):
    queryset = LoanDetails.objects.all()
    serializer_class = LoanDetailsSerializer

class DocumentUploadViewSet(viewsets.ModelViewSet):
    queryset = DocumentUpload.objects.all()
    serializer_class = DocumentUploadSerializer
