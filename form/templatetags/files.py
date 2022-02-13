from django import template
from form.models import UploadModel

register = template.Library()

@register.simple_tag
def files():
    files = UploadModel.objects.all()
    return files

