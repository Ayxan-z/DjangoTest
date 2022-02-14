from django.contrib import admin
from django.urls import path, include
from form import views

urlpatterns = [
    path('', views.UploadView.as_view(), name='fileupload'),
    path('detail/<slug:slug>/<slug:column>', views.detailView, name='detail'),
]
