from autoslug import AutoSlugField
from django.db import models


class UploadModel(models.Model):
    files = models.FileField('Fayl', upload_to='')
    slug = AutoSlugField(populate_from='files', unique=True)
