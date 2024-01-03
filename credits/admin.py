from django.contrib import admin
from .models import CreditPlan, UserCredits

# Register your models here.
admin.site.register(CreditPlan)
admin.site.register(UserCredits)
