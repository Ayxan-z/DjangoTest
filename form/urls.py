from django.contrib import admin
from django.urls import path, include
from form import views

urlpatterns = [
    path('', views.UploadView.as_view(), name='fileupload'),
    path('detail/<slug:slug>/<int:column_index>', views.detailView, name='detail'),
]
