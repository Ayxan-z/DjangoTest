from django.shortcuts import render
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
        