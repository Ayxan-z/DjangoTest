from django import forms
from form.models import UploadModel


class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadModel
        fields = ('files',)

