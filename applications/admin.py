from django.contrib import admin
from .models import Application, PersonalDetails, LoanDetails, DocumentUpload, ApplicationTracker

# Register your models here.

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'user', 'status', 'created_at')
    search_fields = ('tracking_number', 'user__username')

class PersonalDetailsAdmin(admin.ModelAdmin):
    list_display = ('application', 'name', 'national_id')
    search_fields = ('name', 'national_id')

class LoanDetailsAdmin(admin.ModelAdmin):
    list_display = ('application', 'loan_amount', 'vehicle_make', 'vehicle_model')
    search_fields = ('application__tracking_number',)

class DocumentUploadAdmin(admin.ModelAdmin):
    list_display = ('application', 'document_type', 'is_validated')
    search_fields = ('application__tracking_number',)

admin.site.register(Application, ApplicationAdmin)
admin.site.register(PersonalDetails, PersonalDetailsAdmin)
admin.site.register(LoanDetails, LoanDetailsAdmin)
admin.site.register(DocumentUpload, DocumentUploadAdmin)
admin.site.register(ApplicationTracker)


