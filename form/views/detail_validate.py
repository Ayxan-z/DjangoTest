from django.http import HttpResponse
from django.shortcuts import render
from form.models import UploadModel
import pandas as pd
from django.conf import settings
from json import dumps


class DetailValidate():
    
    @staticmethod
    def __openExcelAsDataFrame(data):
        return pd.read_excel(io=str(settings.BASE_DIR) + data[0].files.url)
    
    @staticmethod
    def __openCsvAsDataFrame(data) -> pd.DataFrame:
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
            
        return pd.DataFrame(d)
    
    @staticmethod
    def __dataFrameToHTML(df):
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
        
        return df_html
    
    @staticmethod
    def __dataFrameColumnToJSON(df, column_index):
        x = 0
        graph_data = []
        for i in df[df.columns[column_index]]:
            graph_data.append({ 'x': x, 'y': i })
            x += 1

        return dumps(graph_data)
    
    def createTable(self, slug):
        data = UploadModel.objects.filter(slug=slug)
        try: 
            self.df = self.__openExcelAsDataFrame(data)

        except: 
            try: 
                self.df = self.__openCsvAsDataFrame(data)
                
            except: return HttpResponse("<h2>Fayl oxunanmadı!</h2>")

        df_html = self.__dataFrameToHTML(self.df)
        return df_html

    def createLineGraph(self, column_index) -> dumps or None:
        if self.df.columns.__len__() >= column_index > 0 :
            column_index -= 1
            str_type = str(self.df[self.df.columns[column_index]].dtypes)
                    
            if 'int' in str_type or 'float' in str_type:
                graph_dataJSON = self.__dataFrameColumnToJSON(self.df, column_index)
                return graph_dataJSON
            