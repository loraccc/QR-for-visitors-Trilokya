# generate_qr_code.py
import qrcode

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Retrieve the FRONTEND_URL from environment variables
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:8000/')



def generate_qr_code():
    # Construct the URL for the review form
    # review_url = "http://127.0.0.1:8000/pages/submit-review/"  # Local development URL
    review_url = f"{FRONTEND_URL}pages/submit-review/"  

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(review_url)
    qr.make(fit=True)

    # Create the QR code image
    img = qr.make_image(fill_color="white", back_color="red")

    # Save or display the QR code image as needed
    img.save("static/img/qr_code_review_form.png")


generate_qr_code()
