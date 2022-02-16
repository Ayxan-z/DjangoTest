from django.http import HttpResponse
from django.shortcuts import render
from form.models import UploadModel
import pandas as pd
from django.conf import settings
from json import dumps
from .detail_validate import DetailValidate


def detailView(request, slug, column_index):
    dv = DetailValidate()
    table = dv.createTable(slug)
    
    if type(table) != str: return table
    
    graph = dv.createLineGraph(column_index)
    return render(request,
                'pages/detail.html',
                context={'df_html': table,
                        'graph_dataJSON': graph})
        