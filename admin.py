from django.contrib import admin
from .models import Activity, quotations, Task

admin.site.register(Activity)
admin.site.register(quotations)
admin.site.register(Task)