from django.shortcuts import render, redirect
from .models import UploadedImage  # ✅ correct relative import
from django.core.files.storage import FileSystemStorage

def homepage(request):
    return render(request, 'home.html')

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        uploaded = UploadedImage.objects.create(image=image)
        return render(request, 'upload.html', {'uploaded': uploaded})

    return render(request, 'upload.html')