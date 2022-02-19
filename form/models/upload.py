from autoslug import AutoSlugField
from django.db import models


class UploadModel(models.Model):
    name = models.TextField('Name')
    table = models.TextField('DataFrame')
    slug = AutoSlugField(populate_from='name', unique=True)
