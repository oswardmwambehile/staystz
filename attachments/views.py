

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Attachment
from .forms import AttachmentForm


@login_required
def add_attachment(request):

    # 🔒 BLOCK if attachment already exists
    if Attachment.objects.filter(user=request.user).exists():
        
        return redirect('services-category')  # or profile page

    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.user = request.user
            attachment.is_verified = False
            attachment.save()

            messages.success(request, "Attachment uploaded successfully.")
            return redirect('services-category')
    else:
        form = AttachmentForm()

    return render(request, 'customer/add_attachment.html', {'form': form})



@login_required
def service(request):
    return render(request, 'customer/services.html')
