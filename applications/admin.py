from django.contrib import admin
from .models import Application, PersonalDetails, LoanDetails, DocumentUpload, ApplicationTracker

# Register your models here.

# Admin configuration for Application model
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'user', 'status', 'created_at')  # Display tracking number, user, status, and created date in list view
    list_filter = ('status', 'created_at')  # Filter options for status and created_at
    search_fields = ('tracking_number', 'user__username')  # Searchable by tracking number and username
    readonly_fields = ('tracking_number',)  # Make tracking number read-only

# Admin configuration for PersonalDetails model
class PersonalDetailsAdmin(admin.ModelAdmin):
    list_display = ('application', 'title', 'surname', 'other_names', 'gender', 'national_id')  # Show application, title, surname, other names, gender, and national ID
    search_fields = ('surname', 'other_names', 'national_id')  # Searchable by surname, other names, and national ID

# Admin configuration for LoanDetails model
class LoanDetailsAdmin(admin.ModelAdmin):
    list_display = ('application', 'loan_amount', 'vehicle_make', 'vehicle_model', 'vehicle_year', 'vehicle_cost', 'insurance_premium', 'total_loan_required')  # Display loan details including vehicle details and cost
    search_fields = ('application__tracking_number', 'vehicle_make', 'vehicle_model')  # Searchable by application tracking number, vehicle make, and model
    list_filter = ('vehicle_year',)  # Filter by vehicle year

# Admin configuration for DocumentUpload model
class DocumentUploadAdmin(admin.ModelAdmin):
    list_display = ('application', 'document_type', 'is_validated', 'uploaded_at')  # Display document type, validation status, and upload date
    search_fields = ('application__tracking_number', 'document_type')  # Searchable by tracking number and document type
    list_filter = ('document_type', 'is_validated')  # Filter by document type and validation status

# Register all models to the Django admin site
admin.site.register(Application, ApplicationAdmin)
admin.site.register(PersonalDetails, PersonalDetailsAdmin)
admin.site.register(LoanDetails, LoanDetailsAdmin)
admin.site.register(DocumentUpload, DocumentUploadAdmin)
admin.site.register(ApplicationTracker)
