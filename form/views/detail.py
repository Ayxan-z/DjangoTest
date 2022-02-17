from django.shortcuts import render
from .detail_validate import DetailValidate


def detailView(request, slug, column_index):
    dv = DetailValidate()
    tables = dv.createTable()
    # if type(table) != str: return table
    
    tables_HTML = []
    for value in tables.values():
        if value[0]:
            tables_HTML.append(value[0])

    graph = dv.createLineGraph(slug, column_index)
    if not graph: graph = [None, None]
    
    return render(request,
                'pages/detail.html',
                 context={'tables': tables_HTML,
                        'graph_dataJSON': graph[0],
                        'graph_nameJSON': graph[1]})
        