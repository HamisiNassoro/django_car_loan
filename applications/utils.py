import requests
from io import BytesIO
from reportlab.pdfgen import canvas

def generate_invoice_pdf(application, amount_due):
    """
    Generate a PDF invoice for the given application.

    Args:
        application: The application object for which the invoice is generated.
        amount_due: The amount due for the application.

    Returns:
        A BytesIO object containing the PDF data.
    """
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    # Add content to the PDF
    pdf.drawString(100, 800, "Invoice")
    pdf.drawString(100, 750, f"Application ID: {application.id}")
    pdf.drawString(100, 725, f"Tracking Number: {application.tracking_number}")
    pdf.drawString(100, 700, f"Amount Due: KES {amount_due}")
    pdf.drawString(100, 675, "Thank you for your application.")

    # Finalize the PDF
    pdf.save()
    buffer.seek(0)
    return buffer


def initiate_mpesa_payment(phone_number, amount):
    # Dummy URL and credentials for example
    access_token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    payment_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    consumer_key = "4CelAspFQYfTwtGF0kkq5eMrOSRx5GpUZh7ePmeltqD3TGpH"
    consumer_secret = "MqIl9N9GrrELyJMoSoxWlOlEnlpZ9IwVApgojDJDr0YgBfVoeQEs3YRK9F1gsoPP"
    business_shortcode = 174379
    passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    
    # Access Token
    response = requests.get(access_token_url, auth=(consumer_key, consumer_secret))
    access_token = response.json().get("access_token")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Initiate Payment
    payload = {
        "BusinessShortCode": business_shortcode,
        "Password": f"{business_shortcode}{passkey}",
        "Timestamp": "20221110170100",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": float(amount),  # Convert Decimal to float
        "PartyA": phone_number,
        "PartyB": business_shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://yourdomain.com/mpesa/callback",
        "AccountReference": "Car Loan",
        "TransactionDesc": "Payment for car loan application",
    }
    
    response = requests.post(payment_url, json=payload, headers=headers)
    return response.json()
