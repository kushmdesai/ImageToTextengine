from django.shortcuts import render, redirect
from .models import UploadedImage  # ✅ correct relative import
from django.core.files.storage import FileSystemStorage
from PIL import Image
import pytesseract
from django.core.files.base import ContentFile
from io import BytesIO
from django.shortcuts import render
from .models import UploadedImage
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO

def homepage(request):
    return render(request, 'home.html')

# def upload_image(request):
#     if request.method == 'POST' and request.FILES.get('image'):
#         image = request.FILES['image']
#         uploaded = UploadedImage.objects.create(image=image)
#         return render(request, 'upload.html', {'uploaded': uploaded})

#     return render(request, 'upload.html')

def upload_image(request):
    extracted_text = None

    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        # Save original image
        uploaded = UploadedImage.objects.create(image=image_file)

        # Open image with PIL
        image = Image.open(uploaded.image.path)

        # Use pytesseract to extract text
        extracted_text = pytesseract.image_to_string(image)

        return render(request, 'upload.html', {'uploaded': uploaded, 'extracted_text': extracted_text})

    return render(request, 'upload.html', {'extracted_text': extracted_text})

def download_pdf(request):
    text = request.GET.get('text', '')
    if not text:
        return HttpResponse("No text provided", status=400)

    # Create in-memory bytes buffer
    buffer = BytesIO()

    # Create PDF object, write text to it
    p = canvas.Canvas(buffer)
    text_object = p.beginText(40, 800)  # starting position

    for line in text.splitlines():
        text_object.textLine(line)

    p.drawText(text_object)
    p.showPage()
    p.save()

    buffer.seek(0)

    # Return as a downloadable file
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="extracted_text.pdf"'
    return response