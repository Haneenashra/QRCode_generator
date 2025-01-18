from django.shortcuts import render
import qrcode
from PIL import Image
from io import BytesIO
import base64

def index(request):
    context = {}
    
    if request.method == "POST":
        qr_text = request.POST.get("qr_text", "")
        
        # Ensure there is text to generate QR code
        if qr_text:
            # Create a QRCode object
            qr = qrcode.QRCode(
                version=1, 
                error_correction=qrcode.constants.ERROR_CORRECT_L, 
                box_size=10, 
                border=4
            )

            qr.add_data(qr_text)  # Add the text data to the QR code
            qr.make(fit=True)  # Fit the data into the QR code

            # Generate the QR code image
            qr_image = qr.make_image(fill='black', back_color='white')

            # Save the image to a BytesIO stream
            stream = BytesIO()
            qr_image.save(stream, format='PNG')

            # Convert the image data to base64
            qr_image_data = stream.getvalue()
            qr_image_base64 = base64.b64encode(qr_image_data).decode('utf-8')

            # Add the base64 image data and input text to the context
            context['qr_image_base64'] = qr_image_base64
            context['variable'] = qr_text
        else:
            # Add an error message to the context
            context['error'] = "Please enter text or a link to generate a QR code."

    return render(request, 'index.html', context=context)
