from django.http import HttpResponse
from form.models import UploadModel
import pandas as pd
from django.conf import settings
import json


class DetailValidate():
    
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

        return json.dumps(graph_data)
    
    def createTable(self):
        tables = UploadModel.objects.all()
        
        self.tables_data = {}
        for table in tables:
            df = pd.DataFrame.from_dict(json.loads(table.table))
            HTML_df = [self.__dataFrameToHTML(df, table.slug), df]

            self.tables_data[table.slug] = HTML_df
            
        return self.tables_data

    def createLineGraph(self, slug, column_index) -> json.dumps or None:
        if slug != 'None':
            df = self.tables_data[slug][1]
        
            if df.columns.__len__() >= column_index > 0:
                column_index -= 1
                str_type = str(df[df.columns[column_index]].dtypes)

                if 'int' in str_type or 'float' in str_type:
                    graph_dataJSON = self.__dataFrameColumnToJSON(df, column_index)
                    graph_nameJSON = json.dumps(df[df.columns[column_index]].name)
                    
                    return [graph_dataJSON, graph_nameJSON]
        