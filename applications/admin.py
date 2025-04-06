from django.contrib import admin
from .models import Application, PersonalDetails, LoanDetails, DocumentUpload, ApplicationTracker, JobDetails,  Invoice

# Admin configuration for Application model
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('tracking_number', 'user__username')
    readonly_fields = ('tracking_number',)

# Admin configuration for PersonalDetails model
class PersonalDetailsAdmin(admin.ModelAdmin):
    list_display = ('application', 'title', 'surname', 'other_names', 'gender', 'national_id')
    search_fields = ('surname', 'other_names', 'national_id')

    # Organize fields into sections in the admin form view
    fieldsets = (
        ("Personal Information", {
            'fields': (
                'title', 'surname', 'other_names', 'gender', 'date_of_birth',
                'national_id', 'email_address', 'residential_address', 'personal_no'
            )
        }),
        ("Marital & Kin Details", {
            'fields': (
                'marital_status', 'spouse_name', 'spouse_id', 'next_of_kin',
                'next_of_kin_relationship', 'next_of_kin_id', 'next_of_kin_mobile'
            )
        }),
        ("Disability Information", {
            'fields': ('physical_disability', 'disability_details')
        }),
    )

    # Auto-clear spouse and disability details when saving
    def save_model(self, request, obj, form, change):
        obj.save()  # calls the save method on the model itself

# Admin configuration for JobDetails model
class JobDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'personal_details', 'designation', 'job_group_scale',
        'current_net_salary', 'allocated_amount', 'ministry_department'
    )
    search_fields = ('personal_details__surname', 'designation', 'ministry_department')
    list_filter = ('job_group_scale', 'ministry_department', 'terms_of_service')
    readonly_fields = ('allocated_amount',)

    # Fieldsets for job information grouping
    fieldsets = (
        ("Job Information", {
            'fields': ('designation', 'job_group_scale', 'allocated_amount', 'current_net_salary')
        }),
        ("Appointment Information", {
            'fields': ('date_of_first_appointment', 'date_of_current_appointment', 'terms_of_service', 'contract_end_date')
        }),
        ("Department", {
            'fields': ('ministry_department',)
        }),
    )

    # Calculate allocated amount based on job group scale
    def save_model(self, request, obj, form, change):
        obj.save()  # uses the model's save method, which already calculates allocated amount

# Admin configuration for LoanDetails model
class LoanDetailsAdmin(admin.ModelAdmin):
    list_display = ('application', 'loan_amount', 'vehicle_make', 'vehicle_model', 'vehicle_year', 'vehicle_cost', 'insurance_premium', 'total_loan_required')
    search_fields = ('application__tracking_number', 'vehicle_make', 'vehicle_model')
    list_filter = ('vehicle_year',)

# Admin configuration for DocumentUpload model
class DocumentUploadAdmin(admin.ModelAdmin):
    list_display = ('application', 'document_type', 'is_validated', 'uploaded_at')
    search_fields = ('application__tracking_number', 'document_type')
    list_filter = ('document_type', 'is_validated')

class InvoiceAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('application', 'amount_due', 'created_at', 'is_paid')

    # Add filtering options
    list_filter = ('is_paid', 'created_at')

    # Enable searching by tracking number of the associated application
    search_fields = ('application__tracking_number',)

    # Optional: You can define how the fields are ordered in the list view
    ordering = ('-created_at',)

# Register all models with the admin site
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(PersonalDetails, PersonalDetailsAdmin)
admin.site.register(JobDetails, JobDetailsAdmin)
admin.site.register(LoanDetails, LoanDetailsAdmin)
admin.site.register(DocumentUpload, DocumentUploadAdmin)
admin.site.register(ApplicationTracker)
