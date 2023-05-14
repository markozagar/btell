"""Administrative pages - django builtin."""
from django.contrib import admin
from btell_main import models

# Register your models here.
admin.site.register(models.Profile)
admin.site.register(models.SiteSettings)
