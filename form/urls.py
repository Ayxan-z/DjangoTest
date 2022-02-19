from django.urls import path
from form import views

urlpatterns = [
    path('', views.uploadView, name='fileupload'),
    path('detail/<slug:slug>/<int:column_index>', views.detailView, name='detail'),
]
