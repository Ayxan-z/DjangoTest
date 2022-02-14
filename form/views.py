import os
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView
from .models import UploadModel
from django.urls import reverse
import pandas as pd
from django.conf import settings
from json import dumps


def detailView(request, slug, column):
    data = UploadModel.objects.filter(slug=slug)

    try: df = pd.read_excel(io=str(settings.BASE_DIR) + data[0].files.url)
        
    except: df = pd.read_csv(str(settings.BASE_DIR) + data[0].files.url)

    try:
        columns = list(df.columns)
        columns[columns.index('None')] = 'None1'
        df.columns = columns

    except ValueError: pass

    df_html = df.to_html()
    
    for i in list(df.columns):
        str_i = str(i)
        str_type = str(df[i].dtypes)
        if 'int' in str_type or 'float' in str_type:
            x = df_html.find(f'<th>{str_i}</th>')
            df_html = f'{df_html[:x+4]}<a href="{i}">{str_i}</a>{df_html[len(str_i)+4+x:]}'
    
        else: pass
    
    if column != 'None':
        try:
            str_type = str(df[column].dtypes)
        except KeyError: return HttpResponse("Sütun tapılmadı")
        
        if 'int' in str_type or 'float' in str_type:
            x = 0
            graph_data = []
            for i in df[column]:
                graph_data.append({ 'x': x, 'y': i })
                x += 1

            graph_dataJSON = dumps(graph_data)
            
            return render(request,
                          'pages/detail.html',
                          context={'df_html': df_html, 'graph_dataJSON': graph_dataJSON})
        
    
    return render(request, 'pages/detail.html', context={'df_html': df_html})


class UploadView(CreateView):
    template_name = 'pages/upload.html'
    model = UploadModel
    fields = ('files',)
    
    def get_success_url(self):
        return reverse('fileupload')
    
    def form_valid(self, form):
        if os.path.splitext(form.files.get('files').name)[1] in ['.csv','.xls','.xlsx']:
            return super().form_valid(form)
        
        else: return HttpResponse("Fayl düzgün formatda dəyil!")
            

        


