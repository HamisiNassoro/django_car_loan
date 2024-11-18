from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

def generate_invoice_pdf(application, amount_due):
    template = get_template('invoice_template.html')
    context = {
        'application': application,
        'amount_due': amount_due,
    }
    html = template.render(context)
    buffer = BytesIO()
    pisa.CreatePDF(html, dest=buffer)
    buffer.seek(0)
    return buffer
