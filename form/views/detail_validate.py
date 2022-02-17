from django.http import HttpResponse
from form.models import UploadModel
import pandas as pd
from django.conf import settings
from json import dumps


class DetailValidate():
    
    @staticmethod
    def __openExcelAsDataFrame(url) -> pd.DataFrame:
        return pd.read_excel(io=str(settings.BASE_DIR) + url)
    
    @staticmethod
    def __openCsvAsDataFrame(url) -> pd.DataFrame:
        df = pd.read_csv(str(settings.BASE_DIR) + url)
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
    def __dataFrameToHTML(df, slug):
        df_html = df.to_html()
        
        cnt = 1
        for i in list(df.columns):
            str_i = str(i)
            str_type = str(df[i].dtypes)
            if 'int' in str_type or 'float' in str_type:
                x = df_html.find(f'<th>{str_i}</th>')
                df_html = f'{df_html[:x+4]}<a href="/detail/{slug}/{str(cnt)}">{str_i}</a>{df_html[len(str_i)+4+x:]}'
                style_index = df_html.find('class="dataframe"')
                df_html = df_html[:style_index+17]+' style="display: inline-block; margin-right: 10px;"'+df_html[style_index+17:]
        
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
    
    def createTable(self):
        tables = UploadModel.objects.all()
        # data = UploadModel.objects.filter(slug=slug)
        
        self.tables_data = {}
        for table in tables:
            try: 
                df = self.__openExcelAsDataFrame(table.files.url)
                df = [self.__dataFrameToHTML(df, table.slug), df]

            except: 
                try: 
                    df = self.__openCsvAsDataFrame(table.files.url)
                    df = [self.__dataFrameToHTML(df, table.slug), df]

                except: df = [None, None]

            self.tables_data[table.slug] = df
        return self.tables_data

    def createLineGraph(self, slug, column_index) -> dumps or None:
        if slug != 'None':
            df = self.tables_data[slug][1]
        
            if df.columns.__len__() >= column_index > 0:
                column_index -= 1
                str_type = str(df[df.columns[column_index]].dtypes)

                if 'int' in str_type or 'float' in str_type:
                    graph_dataJSON = self.__dataFrameColumnToJSON(df, column_index)
                    graph_nameJSON = dumps(df[df.columns[column_index]].name)
                    
                    return [graph_dataJSON, graph_nameJSON]
        
        
        # if self.df.columns.__len__() >= column_index > 0 :
        #     column_index -= 1
        #     str_type = str(self.df[self.df.columns[column_index]].dtypes)
                    
        #     if 'int' in str_type or 'float' in str_type:
        #         graph_dataJSON = self.__dataFrameColumnToJSON(self.df, column_index)
        #         return graph_dataJSON
            