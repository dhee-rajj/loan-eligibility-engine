import boto3
from django.shortcuts import render
from django.conf import settings
from .forms import UploadCSVForm
import uuid

def upload_csv(request):
    print("AWS_ACCESS_KEY_ID =", settings.AWS_ACCESS_KEY_ID)
    print("AWS_SECRET_ACCESS_KEY =", settings.AWS_SECRET_ACCESS_KEY)
    print("AWS_STORAGE_BUCKET_NAME =", settings.AWS_STORAGE_BUCKET_NAME)
    print("AWS_REGION =", settings.AWS_REGION)
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['csv_file']
            filename = f"{uuid.uuid4()}.csv"

            s3 = boto3.client('s3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )

            s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, filename)
            return render(request, 'uploader/success.html', {'filename': filename})
    else:
        form = UploadCSVForm()

    return render(request, 'uploader/upload.html', {'form': form})
