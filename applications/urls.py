from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('personal-details/', views.personal_details_view, name='personal_details'),
    path('loan-details/', views.loan_details_view, name='loan_details'),
    path('document-upload/', views.document_upload_view, name='document_upload'),
    path('complete/', views.application_complete_view, name='application_complete'),
    path('enquiry/', views.enquiry_view, name='enquiry'),
    path('faqs/', views.faqs_view, name='faqs'),
]
