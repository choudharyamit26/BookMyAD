from django.contrib import admin
from .models import *
# Register your models here.
admin.site.site_header = 'BookMyAd Admin'
admin.site.index_title = 'Admin Panel BookMyAd'
# admin.site.site_title = 'Django'
admin.site.register(Category)
admin.site.register(City)
admin.site.register(Publication)
admin.site.register(AdType)
admin.site.register(Ad)
admin.site.register(SampleAds)
