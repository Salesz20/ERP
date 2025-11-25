from django.contrib import admin
from .models import Company, Contact, Opportunity, Task

admin.site.register(Company)
admin.site.register(Contact)
admin.site.register(Opportunity)
admin.site.register(Task)
