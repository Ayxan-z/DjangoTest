from multiprocessing import context
import os
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView
from .models import UploadModel
from django.urls import reverse
from django.contrib import messages
import openpyxl
import io


def detailView(request, slug):
    return render(request, 'pages/detail.html', context={'slug': slug})


class UploadView(CreateView):
    template_name = 'pages/upload.html'
    model = UploadModel
    fields = ('files',)
    
    def get_success_url(self):
        # files = UploadModel.objects.all()
        return reverse('fileupload')
        # return reverse('detail', kwargs={
        #     'slug': self.object.slug
        # })
    
    def form_valid(self, form):
        # print(dir(form.files.get('files')))
        # print(type(form.files.get('files').name))
        # print(form.files.get('files').readline())
        
        # wb = openpyxl.load_workbook(io.BytesIO(form.files.get('files').read()))
        # ws = wb['Sheet1']

        # for cells in ws.iter_rows():    
        #     print([cell.value for cell in cells])

        if os.path.splitext(form.files.get('files').name)[1] in ['.csv','.xls','.xlsx']:
            return super().form_valid(form)
        
        else: return HttpResponse("Fayl düzgün formatda dəyil!")
            

        


