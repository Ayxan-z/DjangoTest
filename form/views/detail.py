from django.http import HttpResponse
from django.shortcuts import render
from form.models import UploadModel
import pandas as pd
from django.conf import settings
from json import dumps


def detailView(request, slug, column_index):
    data = UploadModel.objects.filter(slug=slug)

    try: 
        df = pd.read_excel(io=str(settings.BASE_DIR) + data[0].files.url)

    except: 
        try: 
            df = pd.read_csv(str(settings.BASE_DIR) + data[0].files.url)
            cnt = 0
            d = {}
            values = df.values
            ndim = df.values.ndim
            for i in range(ndim):
                df.values[i][0] = df.values[i][0].split(';')
            for i in df.columns[0].split(';'):
                l = []
                for j in range(ndim):
                    try:
                        value = float(values[j][0][cnt])
        
                    except ValueError: value = values[j][0][cnt]
        
                    l.append(value)
                d[i] = l
                cnt += 1
            df = pd.DataFrame(d)
            
        except: return HttpResponse("<h2>Fayl oxunanmadı!</h2>")

    try:
        columns = list(df.columns)
        columns[columns.index('None')] = 'None1'
        df.columns = columns

    except ValueError: pass

    df_html = df.to_html()
    
    cnt = 1
    for i in list(df.columns):
        str_i = str(i)
        str_type = str(df[i].dtypes)
        if 'int' in str_type or 'float' in str_type:
            x = df_html.find(f'<th>{str_i}</th>')
            df_html = f'{df_html[:x+4]}<a href="{str(cnt)}">{str_i}</a>{df_html[len(str_i)+4+x:]}'
    
        else: pass
        cnt += 1
    
    ######################################################################
    # Line Graph
    
    if df.columns.__len__() >= column_index > 0 :
        column_index -= 1
        str_type = str(df[df.columns[column_index]].dtypes)
                
        if 'int' in str_type or 'float' in str_type:
            x = 0
            graph_data = []
            for i in df[df.columns[column_index]]:
                graph_data.append({ 'x': x, 'y': i })
                x += 1

            graph_dataJSON = dumps(graph_data)
            
            return render(request,
                          'pages/detail.html',
                           context={'df_html': df_html,
                                   'graph_dataJSON': graph_dataJSON})
        
    
    return render(request, 'pages/detail.html', context={'df_html': df_html})