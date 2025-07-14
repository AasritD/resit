# services/core_project/app/uploads/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UploadForm
from .models import UploadedFile

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user
            upload.save()
            return redirect('uploads:dashboard')
    else:
        form = UploadForm()

    files = UploadedFile.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'uploads/dashboard.html', {
        'form': form,
        'files': files,
    })
