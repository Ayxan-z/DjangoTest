from django.shortcuts import render
from form.models import UploadModel
from django.contrib import messages
import pandas as pd
from form.forms import UploadForm
from form.models import UploadModel
from io import BytesIO

def saveData(data, df):
    upload = UploadModel(name=data.name, table=df.to_json(orient = 'columns'))
    upload.save()

def csvToXlsx(df) -> pd.DataFrame:
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
            
        return pd.DataFrame(d)

def uploadView(request):
    form = UploadForm()
    
    if request.method == 'POST':
        data = request.FILES.get('files')
        data_read = data.read()

        try:
            df = pd.read_excel(data_read)
            saveData(data, df)
        
        except:
            try:
                df = pd.read_csv(BytesIO(data_read))
                df = csvToXlsx(df)
                saveData(data, df)
            
            except: messages.warning(request, 'Fayl düzgün formatda dəyil!')  

    return render(request, 'pages/upload.html', context={'form': form})
