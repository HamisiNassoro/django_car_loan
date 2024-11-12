from django.urls import path
from . import views

<<<<<<< HEAD
app_name = 'applications'
=======
app_name = 'applications'  # Add this line
>>>>>>> a96d8404 (X)

urlpatterns = [
    path('', views.home, name='home'),                             # Home page
    path('apply/', views.application_form, name='application_form'),  # Multi-step application form
    path('enquiry/', views.enquiry_view, name='enquiry'),           # Enquiry form
    path('faqs/', views.faqs_view, name='faqs'),                    # FAQs
    path('complete/', views.application_complete_view, name='application_complete'),  # Application complete
]
