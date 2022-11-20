import django_tables2 as tables
from .models import Announce


class AnnounceTable(tables.Table):
    class Meta:
        model = Announce
        template_name = "django_tables2/bootstrap.html"
        exclude = ['id']
