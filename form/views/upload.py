import os
from django.shortcuts import render
from django.views.generic import CreateView
from form.models import UploadModel
from django.urls import reverse
from django.contrib import messages

class UploadView(CreateView):
    template_name = 'pages/upload.html'
    model = UploadModel
    fields = ('files',)
    
    def get_success_url(self):
        return reverse('fileupload')
    
    def form_valid(self, form):
        if os.path.splitext(form.files.get('files').name)[1] in ['.csv','.xls','.xlsx']:
            return super().form_valid(form)
        
        else: 
            messages.warning(self.request, 'Fayl düzgün formatda dəyil!')
            return render(self.request, 'pages/upload.html', context={'form': form})