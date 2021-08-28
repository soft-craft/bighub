from django.contrib import admin
from .models import Profile,Primary_leads,Lead_messages,Message_box


# Register your models here.

@admin.register(Profile)
class ProfileAdmin (admin.ModelAdmin):
    list_display = ['user','account_type']


admin.site.register(Primary_leads)
admin.site.register(Lead_messages)
admin.site.register(Message_box)


